""" some filter plugins
"""
import re
import json


def playbook(obj):
    """turn a stdout playbook back into a playbook

    :param obj: the thing to find a playbook in
    :type obj: str or list
    :return: the tasks
    :type: list
    """

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    if isinstance(obj, str):
        lines = obj.splitlines()
    elif not isinstance(obj, list):
        lines = [obj]
    else:
        lines = obj

    entries = []
    chunk = []
    while True:
        line = lines.pop(0)
        if line.startswith("TASK"):
            if chunk:
                entries.append(chunk)
                chunk = []
            chunk.append(line)
        elif line.startswith("PLAY"):
            if chunk:
                entries.append(chunk)
                chunk = []
            chunk.append(line)
            while True:
                line = lines.pop(0)
                if line:
                    chunk.append(line)
                else:
                    break
        elif line:
            chunk.append(line)

        if not lines:
            if chunk:
                entries.append(chunk)
            break
    results = []
    task_regex = re.compile(r"(?P<result>\S+): \[(?P<hostname>\S+)](: FAILED!)? =>")
    for entry in entries:
        if entry[0].startswith("TASK"):
            result = {}
            result["result"] = "unknown"
            result["task"] = re.search(r"\[(.*)\]", entry[0]).group(1)
            result["hostname"] = None
            result["failures"] = "---"
            result["raw_lines"] = entry
            details = " ".join(entry)
            match = task_regex.search(details)
            if match:
                _start, end = match.span()
                cap = match.groupdict()
                result["hostname"] = cap["hostname"]
                result["details"] = cap
                try:
                    json_result = json.loads(details[end:])
                    result["summary"] = json_result
                except json.decoder.JSONDecodeError as _exc:
                    pass

                if cap["result"] == "fatal":
                    if "ignoring" in details:
                        result["result"] = "ignored"
                        result["failures"] = 0
                    else:
                        result["result"] = cap["result"]
                        result["failures"] = 1
                else:
                    result["result"] = cap["result"]
                    result["failures"] = 0

            result["result"] = result["result"].upper()
            results.append(result)
    return results


filters = {"playbook": playbook}
