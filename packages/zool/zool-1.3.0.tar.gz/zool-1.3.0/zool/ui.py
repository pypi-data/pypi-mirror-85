""" the main ui renderer
"""
import curses
import logging
import re
import signal
import textwrap
from itertools import chain
from math import floor


import yaml

from pygments import highlight, lexers, formatters
from zool.utils import convert_percentages, template


try:
    from yaml import CDumper as Dumper

    HAS_LIB_YAML = True
except ImportError:
    from yaml import Dumper

    HAS_LIB_YAML = False


# assuming 16 colors here, use mod curses.COLORS to fix if 8
COLUMN_COLORS = [3, 4, 5, 6, 11, 12, 13, 14]
WORD_TO_COLOR = {
    "success": 10,
    "failure": 9,
    "post_failure": 9,
    "ok": 10,
    "changed": 10,
    "fatal": 9,
    "ignored": 11,
    "pending": 6,
    "skipping": 14,
    "skipped": 14,
    "unknown": 8,
}

CURSES_STYLES = {
    1: curses.A_BOLD,
    2: curses.A_DIM,
    3: curses.A_ITALIC,
    4: curses.A_UNDERLINE,
    5: curses.A_BLINK,
    6: curses.A_BLINK,
    7: curses.A_REVERSE,
    8: curses.A_INVIS,
}

STND_KEYS = {
    "^f/PgUp": "page up",
    "^b/PgDn": "page down",
    "\u2191\u2193": "scroll",
    "esc": "back",
    "[0-9]": "goto",
    ":help": "help",
}

XFORMS = {"yaml": "_to_yaml"}

D_XFORM = "yaml"
D_LEXER = "YamlJinjaLexer"


class TimeoutException(Exception):
    """A custom exception for a timeout"""

    def __init__(self, *args, **kwargs):
        # pylint: disable=super-init-not-called
        pass


def signal_handler(signum, frame):
    """a custom signal handler when the time runs out"""
    raise TimeoutException()


class Ui:
    """The main UI class"""

    # pylint: disable=too-few-public-methods
    def __init__(self, screen_miny, pbar_width):
        """init

        :param screen_miny: The minimum screen height
        :type screen_miny: int
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("libyaml support: %s", HAS_LIB_YAML)
        self._pbar_width = pbar_width
        self._screen_miny = screen_miny

        curses.curs_set(0)

        self._formatter = "Terminal256Formatter"
        self._prefix_color = curses.color_pair(8)
        self._set_colors()

        self._screen = curses.initscr()
        self.refresh = 0

    @property
    def _screen_w(self):
        """return the screen width, less 1 so it's the usable space"""
        return self._screen.getmaxyx()[1] - 1

    @property
    def _screen_h(self):
        """return the screen height, or notify if too small"""
        while True:
            if self._screen.getmaxyx()[0] >= self._screen_miny:
                return self._screen.getmaxyx()[0] - 1
            curses.flash()
            curses.beep()
            self._screen.refresh()

    def _set_colors(self):
        """Set the colors for curses
        if 8, set the menu prefix < 8 and the formatter to simple
        """
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i, i, -1)
        if curses.COLORS == 8:
            self._formatter = "TerminalFormatter"
            self._prefix_color = curses.color_pair(0)

    def _add_line(self, lineno, line):
        """add a line to the screen
        the format of a line is [(x, s, c), (x, s, c)...]
        where x is the column, s is the string, and c is the color
        this allows for mulitple colored text at different cols
        trim as needed, just in case, during quick resizes the data
        may be stale compared to the current screen size

        :param lineno: The line number to draw on
        :type lineno: int
        :param line: a list of string tuples
        :type line: list
        """
        if line:
            self._screen.move(lineno, 0)
            for entry in line:
                if entry[0] < self._screen_w:
                    current = entry[1]
                    revised = entry[1][0 : self._screen_w - entry[0]]
                    if current != revised:
                        entry[1] = revised
                    self._screen.addstr(lineno, *entry)

    @staticmethod
    def _ansi_to_curses(line):
        """Convert ansible color codes to curses colors

        :param line: A string with ansi colors
        :type line: string
        :return: A list of str tuples [(x, s, c), (x, s, c)...]
        :rtype: list
        """
        printable = []
        ansi_regex = re.compile(r"(\x1b\[[\d;]*m)")
        color_regex = re.compile(r"\x1b\[(?P<action>(38;5|39);)?(?P<color>\d+)(;(?P<style>\d+))?m")
        parts = ansi_regex.split(line)
        colno = 0
        color = None
        style = None
        while parts:
            part = parts.pop(0)
            if part:
                match = color_regex.match(part)
                if match:
                    cap = match.groupdict()
                    cnum = int(cap["color"])
                    if cap["action"] == "39;":
                        color = None
                    elif cap["action"] == "38;5;":
                        color = curses.color_pair(cnum % curses.COLORS)
                    elif not cap["action"]:
                        ansi_16 = list(chain(range(30, 38), range(90, 98)))
                        color = ansi_16.index(cnum) if cnum in ansi_16 else None
                        color = curses.color_pair(cnum % curses.COLORS)
                    if cap["style"] and color:
                        style = CURSES_STYLES[int(cap["style"])]
                else:
                    if color and style:
                        tupl = [colno, part, color | style]
                    elif color:
                        tupl = [colno, part, color]
                    else:
                        tupl = [colno, part]
                    if part:
                        printable.append(tupl)
                    colno += len(part)
        return printable

    @staticmethod
    def _distribute(available, weights):
        """distrubute some available
        across a list of numbers

        :param available: the total
        :type available: int
        :param weights: numbers
        :type weights: list of int
        """
        distributed_amounts = []
        total_weights = sum(weights)
        for weight in weights:
            weight = float(weight)
            pcent = weight / total_weights
            distributed_amount = round(pcent * available)
            distributed_amounts.append(distributed_amount)
            total_weights -= weight
            available -= distributed_amount
        return distributed_amounts

    def _footer(self, key_dict):
        """build a footer from the key dict
        spread the columns out evenly

        :param key_dict: all the keys and values
        :type key_dict: dict
        """
        colws = [len("{k}: {v}".format(k=str(k), v=str(v))) for k, v in key_dict.items()]
        gap = floor((self._screen_w - sum(colws)) / len(key_dict))
        adj_colws = [c + gap for c in colws]
        col_starts = [0]
        for idx, colw in enumerate(adj_colws):
            col_starts.append(colw + col_starts[idx])
        footer = []
        for idx, key in enumerate(key_dict):
            left = key[0 : adj_colws[idx]]
            right = " {v}".format(v=key_dict[key])
            right = right[0 : adj_colws[idx] - len(key)]
            footer.append([col_starts[idx], left, curses.A_REVERSE])
            footer.append([col_starts[idx] + len(left), right])
        return footer

    def _display(self, lines, heading=None, key_dict=None):
        # pylint: disable=too-many-branches
        """show something on the screen

        :param lines: The lines to show
        :type lines: list
        :param heading: the headers
        :type heading: list
        :param key_dict: any suplimental key to show
        :type key_dict: dict
        """
        heading = heading or []
        key_dict = key_dict or {}
        max_lines = self._screen_h - 1
        cursor_at = max_lines
        footer = self._footer(dict(STND_KEYS, **key_dict))
        signal.signal(signal.SIGALRM, signal_handler)
        while True:
            self._screen.erase()
            if heading:
                self._add_line(0, heading)
            self._add_line(self._screen_h, footer)
            for lineno, line in enumerate(
                lines[cursor_at - max_lines : cursor_at], int(bool(heading))
            ):
                self._add_line(lineno, line)
            self._screen.refresh()

            try:
                signal.alarm(self.refresh)
                curses.flushinp()
                key = curses.keyname(self._screen.getch()).decode()
                signal.alarm(0)
            except TimeoutException as _exc:
                key = "KEY_F(5)"

            if key == "KEY_RESIZE":
                return key

            if key == "KEY_DOWN" and cursor_at < len(lines):
                cursor_at += 1

            elif key == "KEY_UP" and cursor_at != max_lines:
                cursor_at -= 1

            elif key in ["^F", "KEY_NPAGE"] and not cursor_at > len(lines):
                cursor_at += max_lines

            elif key in ["^B", "KEY_PPAGE"] and not cursor_at < max_lines:
                cursor_at -= max_lines
                if cursor_at < max_lines:
                    cursor_at = max_lines

            elif key in ["^[", "\x1b"]:
                return None

            elif key in [str(x) for x in range(0, 10)] + [
                "+",
                "-",
                "KEY_F(5)",
            ]:
                return key

            elif key == ":":
                curses.echo()
                self._add_line(self._screen_h, [[0, ":"]])
                self._screen.clrtoeol()
                entry = self._screen.getstr(self._screen_h, 1, self._screen_w).decode()
                curses.noecho()
                if match := re.match(r"^refresh (?P<time>\d+)", entry):
                    self.refresh = int(match.groupdict()["time"])
                elif entry != "":
                    return entry

    def _table(self, dicts, cols):
        # pylint: disable=too-many-locals
        """Build a text table from a list of dicts

        :param dicts: A list of dicts
        :type dicts: list
        :param cols: The columns (keys) to use in the dicts
        :type cols: list of strings
        """
        sample_prefix = "100|"
        convert_percentages(dicts, cols, self._pbar_width)
        lines = [[str(d.get(c)) for c in cols] for d in dicts]
        colws = [max([len(str(v)) for v in c]) for c in zip(*lines + [cols])]
        # add a space
        colws = [c + 1 for c in colws]

        available = self._screen_w - len(sample_prefix)
        adj_colws = self._distribute(available, colws)

        col_starts = [0]
        for idx, colw in enumerate(adj_colws):
            col_starts.append(colw + col_starts[idx])

        header = []
        for idx, entry in enumerate(cols):
            header.append(
                [
                    col_starts[idx] + len(sample_prefix),
                    entry[0 : adj_colws[idx]].upper(),
                ]
            )

        results = []
        for index, line in enumerate(lines):
            result = []
            line_prefix = "{index}|".format(index=str(index).rjust(3))
            result.append([0, line_prefix, self._prefix_color])
            for colno, coltext in enumerate(line):
                if color := WORD_TO_COLOR.get(coltext.lower()):
                    color = curses.color_pair(color % curses.COLORS)
                else:
                    column_color = COLUMN_COLORS[colno % len(COLUMN_COLORS)]
                    color = column_color % curses.COLORS
                    color = curses.color_pair(color)
                print_at = col_starts[colno] + len(line_prefix)
                result.append([print_at, coltext[0 : adj_colws[colno]], color])
            results.append(result)
        return header, results

    def _show_menu(self, current, columns):
        while True:
            heading, lines = self._table(current, columns)
            entry = self._display(lines=lines, heading=heading)
            if entry:
                common = self._check_common_keys(entry)
                if common:
                    return common
                if entry.isnumeric():
                    return {"action": "select", "value": int(entry)}
            else:
                self._screen.erase()
                self._screen.refresh()
                return {"action": "navigate", "value": "previous"}

    @staticmethod
    def _check_common_keys(entry):
        """Check the user entry against some keys
        common to all screens

        :param entry: The user's input
        :type entry: str
        :return: A dict of the action to be taken
        :rtype: dict or None
        """
        if entry == "q":
            return {"action": "quit", "value": None}
        if entry == "KEY_F(5)":
            return {"action": "refresh", "value": None}
        if entry in ["h", "help"]:
            return {"action": "help", "value": None}
        if entry in ["log"]:
            return {"action": "log", "value": None}
        return None

    @staticmethod
    def _to_yaml(obj):
        obj = yaml.dump(obj, sort_keys=False, Dumper=Dumper)
        return obj

    def _highlight(self, obj, formatter, lexer):
        highlit = highlight(obj, getattr(lexers, lexer)(), getattr(formatters, formatter)())
        lines = [self._ansi_to_curses(line) for line in highlit.splitlines()]
        return lines

    def _format(self, obj, formatter, xform, lexer, wrap):
        # pylint: disable=too-many-arguments
        if xform:
            obj = getattr(self, XFORMS[xform])(obj)
        if wrap:
            obj = [
                textwrap.fill(
                    l,
                    initial_indent="",
                    subsequent_indent=" " * 4,
                    width=self._screen_w,
                )
                for l in obj.splitlines()
            ]
            obj = "\n".join(obj)
        if lexer:
            obj = self._highlight(obj, formatter, lexer)
        return obj

    def _show_obj_from_list(self, objs, index, formatter, xform, lexer, wrap):
        # pylint: disable=too-many-arguments
        lines = self._format(objs[index], formatter, xform, lexer, wrap)
        while True:
            if len(objs) > 1:
                heading = [[0, "ENTRY NUMER {index}".format(index=index)]]
            else:
                heading = None
            entry = self._display(
                lines,
                heading=heading,
                key_dict={
                    "+": "previous",
                    "-": "next",
                },
            )

            if entry:
                common = self._check_common_keys(entry)
                if common:
                    return common

                if entry.startswith("{{"):
                    result = template(entry, objs[index])
                    if "|playbook" in entry and result:
                        return {"action": "playbook", "value": result}
                    return {"action": "template", "value": result}

                if entry in ["p", "-"]:
                    index = (index - 1) % len(objs)
                    lines = self._format(objs[index], formatter, xform, lexer, wrap)
                elif entry in ["n", "+"]:
                    index = (index + 1) % len(objs)
                    lines = self._format(objs[index], formatter, xform, lexer, wrap)
                elif entry.isnumeric():
                    index = int(entry) % len(objs)
                    lines = self._format(objs[index], formatter, xform, lexer, wrap)
                elif entry == "KEY_RESIZE" and wrap:
                    lines = self._format(objs[index], formatter, xform, lexer, wrap)

            else:
                self._screen.erase()
                self._screen.refresh()
                return {"action": "navigate", "value": "previous"}

    def show(
        self,
        obj,
        index=None,
        columns=None,
        formatter=None,
        xform=D_XFORM,
        lexer=D_LEXER,
        wrap=True,
    ):
        """Show something on the screen

        :param obj: The inbound object
        :type obj: anything
        :param index: When obj is a list, show this entry
        :type index: int
        :param columns: When obj is a list of dicts, use these keys for menu columns
        :type columns: list
        :param formatter: The pygments formatter https://pygments.org/docs/formatters/
        :type formatter: string
        :param xform: The way to serialize the obj
        :type xform: string
        :param lexer: A pygments lexer https://pygments.org/docs/lexers/
        :type lexer: str
        """
        # pylint: disable=too-many-arguments
        columns = columns or []
        formatter = formatter or self._formatter
        if index is not None:
            result = self._show_obj_from_list(obj, index, formatter, xform, lexer, wrap)
        elif columns:
            result = self._show_menu(obj, columns)
        else:
            result = self._show_obj_from_list([obj], 0, formatter, xform, lexer, wrap)
        self.logger.debug("Returning: %s", result)
        return result
