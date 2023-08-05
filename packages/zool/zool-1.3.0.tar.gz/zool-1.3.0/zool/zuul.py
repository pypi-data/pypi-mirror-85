""" do some zuul stuff

TODO Sees if we can get the target url populated
eg https://api.github.com/repos/ansible-collections/community.vmware/statuses/61f939194ba723d43381b4cbd2bd0bae3bace33b
"""
import json
import logging
import requests
from lxml import html
from zool.utils import to_list


class Zuul:
    """the zuul class, get and resturctures zuul data"""

    def __init__(self, *_args, **kwargs):
        """start

        :param gh: a github instance
        :type gh: zool.github
        :param host: The zuul host
        :type host: str
        :param tenant: the zuul tenant
        :type tenant: str
        """
        self._host = kwargs["zuul_host"]
        self._tenant = kwargs["zuul_tenant"]
        self._organization = kwargs["organization"]
        self._collection = kwargs["collection"]
        self._gh_host = kwargs["gh_host"]
        self._logger = logging.getLogger(__name__)
        self._session = requests.Session()

    def jobs(self, pull):
        """the jobs given a pr

        :param pull: a github pull request
        :type pull: dict
        :return: the jobs
        :rtype: list
        """
        base_url = "https://{host}/{organization}/{repo}".format(
            host=self._gh_host,
            organization=self._organization,
            repo=self._collection,
        )
        url = "{base_url}/pull/{num}/checks".format(
            base_url=base_url,
            num=pull["number"],
        )

        try:
            page = self._session.get(url)
            page.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            self._logger.info(exc)
            return []

        tree = html.fromstring(page.content)
        tree.make_links_absolute(base_url)

        check_runs = []
        for element, _attribute, link, _pos in tree.iterlinks():
            if "check_run_id=" in link:
                check_run = {
                    "title": element.getparent().attrib["title"],
                    "href": link,
                }
                check_runs.append(check_run)
        jobs = []
        for check_run in check_runs:
            jobs.extend(self._job_from_check_run(check_run))
        return jobs

    def _job_from_check_run(self, check_run):

        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches

        try:
            page = self._session.get(check_run["href"])
            page.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            self._logger.info(exc)
            return []

        tree = html.fromstring(page.content)
        link = None
        for element, _attribute, link, _pos in tree.iterlinks():
            click = element.get("data-hydro-click")
            if click:
                jclick = json.loads(click)
                if jclick["payload"].get("link_text") == "View more details on":
                    break

        if not link:
            self._logger.error("Unaable to find the link to zuul pull in: %s", check_run)
            return []

        job_id = link.split("/")[-1]
        if "change" in link:
            url = "https://{host}/api/tenant/{tenant}/status/change/{id}".format(
                host=self._host, tenant=self._tenant, id=job_id
            )
            kind = "jobs"
            log_key = "report_url"
            name = "name"

        if "buildset" in link:
            url = "https://{host}/api/tenant/{tenant}/buildset/{id}".format(
                host=self._host, tenant=self._tenant, id=job_id
            )
            kind = "builds"
            log_key = "log_url"
            name = "job_name"

        try:
            page = self._session.get(url)
            page.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            self._logger.info(exc)
            return []

        blob = to_list(page.json())

        jobs = []
        for entry in blob:
            for job in entry.get(kind, []):
                if kind == "builds":
                    percent = "100%"
                else:
                    elapsed = job.get("elapsed_time")
                    remaining = job.get("remaining_time")
                    if elapsed is not None and remaining is not None:
                        percent = str(int(elapsed / (elapsed + remaining) * 100)) + "%"
                    else:
                        percent = "0%"
                jobs.append(
                    {
                        "result": job["result"],
                        "check run": check_run["title"],
                        "jobs": job[name],
                        "voting": job["voting"],
                        "% complete": percent,  # job.get("remaining_time", "Done"),
                        "_url": job[log_key],
                    }
                )
        return jobs

    def runs(self, job):
        """get the runs for a job

        :param job:
        :type job: zuul job
        :return: the job runs
        :rtype: list
        """
        url = job.get("_url")
        # TODO: do something with this
        if not url or url.startswith("finger://"):
            self._logger.error("missing or unusable url in job %s", job)
            return []
        try:
            page = self._session.get(url + "job-output.json")
            page.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            self._logger.info(exc)
            return []
        runs = page.json()
        result = []
        for zrun in runs:
            if zrun["stats"]:
                run = {}
                run["result"] = None
                run["failures"] = sum(
                    v["failures"] for h, v in zrun["stats"].items() if v["failures"]
                )
                run["runs"] = zrun["playbook"]
                run["result"] = "FAILURE" if run["failures"] else "SUCCESS"
                run["_plays"] = zrun["plays"]
                result.append(run)
        return result

    @staticmethod
    def plays(plays):
        """extract the plays

        :param plays: The zuul plays
        :type plays: list
        :return: the formatted plays
        :rtype: list
        """
        result = []
        for zplay in plays["_plays"]:
            play = {}
            play["result"] = None
            play["plays"] = zplay["play"]["name"]
            failures = 0
            for task in zplay["tasks"]:
                value = {}
                for _host, value in task["hosts"].items():
                    if value.get("failed"):
                        failures += 1
                if "results" in value:
                    failures += len([r for r in value["results"] if r.get("failed")])
            play["failures"] = failures
            play["result"] = "FAILURE" if play["failures"] else "SUCCESS"
            play["_tasks"] = zplay["tasks"]
            result.append(play)
        return result

    @staticmethod
    def tasks(play):
        """extract the tasks from the play

        :param play: a zuul play
        :type play: list
        :return: the tasks
        :rtype: list
        """
        result = []
        for ztask in play["_tasks"]:
            for hostname, value in ztask["hosts"].items():
                task = {}
                task["hostname"] = hostname
                task["task"] = ztask["task"]["name"] or value["action"]
                failures = 0
                if value.get("failed"):
                    failures += 1
                if "results" in value:
                    failures += len([r for r in value["results"] if r.get("failed")])
                if value.get("skipped"):
                    task["result"] = "skipped"
                elif failures:
                    task["result"] = "fatal"
                else:
                    task["result"] = "ok"
                task["failures"] = failures
                task["result"] = task["result"].upper()
                task.update(value)
                result.append(task)
        return result
