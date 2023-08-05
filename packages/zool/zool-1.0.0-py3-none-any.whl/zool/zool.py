#!/usr/bin/env python3
""" the zool
"""
from curses import wrapper
import os
import sys
import tempfile
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import logging

from zool.github import Github
from zool.zuul import Zuul
from zool.ui import Ui

HELP = """
## GENERAL
---------------------------------------------------------
f/PgUp              Page up
^b/PgDn             Page down
\u2191\u2193        Scroll up/down
:help               This page
:log                Review the current log file
:refresh n          Refresh page every n seconds

## MENUS
---------------------------------------------------------
esc                 Go back
[0-9]               Go to menu item
:number             Go to menu item

## TASKS
---------------------------------------------------------
[0-9]               Goto task number
:number             Goto task number
+                   Next task
-                   Previous task
:{{ key|playbook }} Parse the key's value as a playbook
:{{ key|filter }}   Template the key's value
"""


class Step:

    # pylint: disable=too-many-instance-attributes
    """One step in the flow of things"""

    def __init__(self, name, tipe, func):
        self._index = None
        self._index_changed = False
        self._value = None
        self._value_changed = False
        self.name = name
        self.type = tipe
        self.func = func
        self.previous = None
        self.next = None
        self.columns = COLUMNS.get(self.name, [])

    @property
    def changed(self):
        """return if this has changed

        :return: if this has changed
        :rtype: bool
        """
        return self._index_changed or self._value_changed

    @changed.setter
    def changed(self, value):
        """set the changed value

        :param value: The value to set
        :type value: something that can be booled
        """
        self._value_check(value, bool)
        self._index_changed = value
        self._value_changed = value

    @property
    def index(self):
        """return the index

        :return: index
        :rtype: should be int
        """
        return self._index

    @index.setter
    def index(self, index):
        """set the index

        :param index: the index
        :type index: intable index
        """
        self._value_check(index, int)
        self._index_changed = self._index != index
        self._index = int(index)

    @property
    def selected(self):
        """return the selected item

        :return: the selected item
        :rtype: obj
        """
        try:
            return self._value[self._index]
        except AttributeError as _exc:
            return None

    @property
    def value(self):
        """return the value

        :return: the value
        :rtype: list
        """
        return self._value

    @value.setter
    def value(self, value):
        """set the value and changed is needed

        :param value: list
        :type value: list
        """
        self._value_check(value, list)
        self._value_changed = self._value != value
        self._value = value

    @staticmethod
    def _value_check(value, want):
        """check some expect type against a value"""
        if not isinstance(value, want):
            raise ValueError("wanted {want}, got {value}".format(want=want, value=type(value)))


COLUMNS = {
    "pulls": ["author", "number", "pulls"],
    "jobs": ["result", "check run", "jobs", "voting", "% complete"],
    "runs": ["result", "runs", "failures"],
    "plays": ["result", "plays", "failures"],
    "tasks": ["result", "hostname", "task", "failures"],
    "task": [],
}


class Zool:
    """The zool class

    :param screen: A curses screen
    :type screen: curses screen
    :param args: The cli arguments
    :type args: argparse namespace
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods

    def __init__(self, screen, args):
        self.logger = logging.getLogger(__name__)
        self._screen = screen
        self._args = args
        self._gh = Github(**vars(args))
        self._zuul = Zuul(**vars(args)) #gh=self._gh, host=args.zuul_host, tenant=args.zuul_tenant)
        self._ui = Ui(screen_miny=3, pbar_width=args.pbar_width)

        self._pulls = Step("pulls", "menu", self._gh.pulls)
        self._jobs = Step("jobs", "menu", self._zuul.jobs)
        self._runs = Step("runs", "menu", self._zuul.runs)
        self._plays = Step("plays", "menu", self._zuul.plays)
        self._tasks = Step("tasks", "menu", self._zuul.tasks)
        self._task = Step("task", "content", None)
        self._parsed_playbook = Step("parsed_playbook", "menu", None)
        self._parsed_task = Step("parsed_task", "content", None)

        self._pulls.previous = self._pulls
        self._pulls.next = self._jobs

        self._jobs.previous = self._pulls
        self._jobs.next = self._runs

        self._runs.previous = self._jobs
        self._runs.next = self._plays

        self._plays.previous = self._runs
        self._plays.next = self._tasks

        self._tasks.previous = self._plays
        self._tasks.next = self._task

        self._task.previous = self._tasks
        self._task.next = None

        self._parsed_playbook.previous = self._task
        self._parsed_playbook.next = self._parsed_task
        self._parsed_playbook.columns = COLUMNS["tasks"]

        self._parsed_task.previous = self._parsed_playbook
        self._parsed_task.next = None

        self.loop()

    def _populate(self, step):
        if step == step.previous:
            if step.value is None:
                self.logger.info("Running %s() for step %s", step.func.__name__, step.name)
                step.value = step.func()
            return

        if step.func is None:
            return

        if step.previous.selected:
            if step.previous.changed or step.value is None:
                self.logger.info("Running %s() for step %s", step.func.__name__, step.name)
                step.value = step.func(step.previous.selected)
        return

    def loop(self):
        """The main ui loop"""

        # pylint:disable=too-many-branches
        step = self._pulls
        while True:
            if step.type == "menu":
                self._populate(step)
                result = self._ui.show(obj=step.value, columns=step.columns)

            elif step.type == "content":
                result = self._ui.show(obj=step.previous.value, index=step.previous.index)

            step.previous.changed = False

            if result["action"] != "refresh":
                self._ui.refresh = 0

            if result["action"] == "select":
                step.index = result["value"]
                step = step.next
            elif result["action"] == "navigate":
                if result["value"] == "previous":
                    step = step.previous
            elif result["action"] == "template":
                while result["action"] == "template":
                    result = self._ui.show(obj=result["value"])
            elif result["action"] == "playbook":
                self._parsed_playbook.value = result["value"]
                step = self._parsed_playbook
            elif result["action"] == "quit":
                sys.exit(0)
            elif result["action"] == "help":
                self._ui.show(obj=HELP, xform=None, lexer="MarkdownLexer")
            elif result["action"] == "log":
                with open(self._args.logfile) as fhand:
                    content = fhand.read()
                self._ui.show(obj=content, xform=None, lexer="TextLexer")
            elif result["action"] == "refresh":
                step.value = None


def setup_logger(args):
    """set up the logger

    :param args: The cli args
    :type args: argparse namespace
    """
    if os.path.exists(args.logfile):
        with open(args.logfile, "w"):
            pass
    logger = logging.getLogger()
    hdlr = logging.FileHandler(args.logfile)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s Module: '%(module)s' Function: '%(funcName)s' %(message)s"
    )
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(getattr(logging, args.loglevel.upper()))


def main():
    """start the fun here"""
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-c",
        "--collection",
        help="The collection name, used as the githubh repo (ie ansible.netcommon)",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-o",
        "--organization",
        default="ansible-collections",
        help="The Github organization",
        type=str,
    )
    parser.add_argument(
        "-u",
        "--username",
        default=os.popen("git config user.name").read().strip("\n"),
        help="The Github username for the token",
        type=str,
    )
    parser.add_argument(
        "-t",
        "--token",
        default=None,
        help="Github personal access token (env var GH_TOKEN)",
        type=str,
    )
    parser.add_argument(
        "-l",
        "--log-level",
        default="info",
        dest="loglevel",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level",
        type=str,
    )

    parser.add_argument(
        "-f",
        "--log-file",
        default=tempfile.gettempdir() + "/zool.log",
        dest="logfile",
        help="Log file location",
        type=str,
    )

    parser.add_argument(
        "-zh",
        "--zuul-host",
        default="dashboard.zuul.ansible.com",
        dest="zuul_host",
        help="The zuul hostname",
        type=str,
    )

    parser.add_argument(
        "-zt",
        "--zuul-tenant",
        default="ansible",
        dest="zuul_tenant",
        help="The zuul tenant",
        type=str,
    )

    parser.add_argument(
        "-gh",
        "--github_host",
        default="github.com",
        dest="gh_host",
        help="The github host (browser)",
        type=str,
    )

    parser.add_argument(
        "-gha",
        "--github_api_host",
        default="api.github.com",
        dest="gh_api_host",
        help="The github host (api)",
        type=str,
    )

    parser.add_argument(
        "-p",
        "--pbar-width",
        default=10,
        dest="pbar_width",
        help="The width of the progress bars",
        type=int,
    )

    args = parser.parse_args()
    args.token = os.environ.get("GH_TOKEN")
    os.environ.setdefault("ESCDELAY", "25")
    setup_logger(args)
    wrapper(Zool, args)


if __name__ == "__main__":
    main()
