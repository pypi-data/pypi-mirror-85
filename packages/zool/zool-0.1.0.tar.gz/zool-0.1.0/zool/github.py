""" A simple github worker
"""
import logging
import sys
import requests


class Github:
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
        self.logger = logging.getLogger(__name__)

    def pulls(self):
        """get the pull requests for a repo"""
        url = "https://{host}/repos/{org}/{col}/pulls".format(
            host=self._api_host, org=self._organization, col=self._collection
        )
        if self._username and self._token:
            self.logger.info("Using github credentials")
            auth = requests.auth.HTTPBasicAuth(self._username, self._token)
        else:
            self.logger.info("No github crednetials, default github rate limits are in effect")
            auth = None

        try:
            page = requests.get(url, auth=auth)
            page.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            self.logger.info(exc)
            msg = (
                "Error when collecting pull requests, check the org, collection, and permissions: "
            )
            sys.exit(msg + str(exc))

        self.logger.debug(page.headers)
        pulls = page.json()
        result = []
        for pull in pulls:
            entry = {
                "author": pull["user"]["login"],
                "pulls": pull["title"],
                "number": pull["number"],
            }
            result.append(entry)
        return result

    def get_checks_page(self, pull_num):
        """get the check from the gh ui

        :param pull_num: the pr number
        :type pull_num: int
        """
        url = "https://{host}/{organization}/{repo}/pull/{num}/checks".format(
            host=self._host,
            num=pull_num,
            organization=self._organization,
            repo=self._collection,
        )
        page = requests.get(url)
        return page
