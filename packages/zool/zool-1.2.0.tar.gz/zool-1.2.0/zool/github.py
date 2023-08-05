""" A simple github worker
"""
import logging
import sys
import requests


class Github:

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """class Github"""

    def __init__(self, *_args, **kwargs):
        """init

        :param username: The github username
        :type username: str
        :param token: Teh github personal access token
        :type token: str
        :param organization: the gh org
        :type orgnaization: str
        :param collection: the collection (repo)
        :type collection: str
        :param gh_host: the github UI host
        :type gh_host: str
        :param gh_api_host: the github api host
        :type gh_api_host: str
        """
        self._username = kwargs["username"]
        self._token = kwargs["token"]
        self._organization = kwargs["organization"]
        self._collection = kwargs["collection"]
        self._host = kwargs["gh_host"]
        self._api_host = kwargs["gh_api_host"]
        self._logger = logging.getLogger(__name__)
        self._session = requests.Session()

    def pulls(self):
        """get the pull requests for a repo"""

        url = "https://{host}/repos/{org}/{col}/pulls".format(
            host=self._api_host, org=self._organization, col=self._collection
        )
        if self._username and self._token:
            self._logger.info("Using github credentials")
            auth = requests.auth.HTTPBasicAuth(self._username, self._token)
        else:
            self._logger.info("No github crednetials, default github rate limits are in effect")
            auth = None

        try:
            page = self._session.get(url, auth=auth)
            page.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            self._logger.info(exc)
            if page:
                self._logger.info(page.headers)

            msg = (
                "Error when collecting pull requests, check the org, collection, and permissions: "
            )
            sys.exit(msg + str(exc))

        pulls = page.json()
        result = []
        for pull in pulls:
            entry = {
                "author": pull["user"]["login"],
                "pulls": pull["title"],
                "number": pull["number"],
                "status": self._get_statuses(pull, auth).upper(),
            }
            result.append(entry)
        return result

    def _get_statuses(self, pull, auth):
        """get individual status

        :param pull: a pr
        :type pull: dict
        :param auth: an auth tuple
        :type auth: requests.auth
        """
        try:
            self._logger.debug("Getting status for %s", pull["title"])
            page = self._session.get(pull["statuses_url"], auth=auth)
            page.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            self._logger.info(exc)

        statuses = page.json()
        stati = [status["state"] for status in statuses]

        if "failure" in stati:
            return "failure"
        if "pending" in stati:
            return "pending"
        if all(s == "success" for s in stati):
            return "success"
        return "unknown"
