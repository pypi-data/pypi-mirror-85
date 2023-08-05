""" some utilities that didn't fit elsewhere
"""
import json
import logging
import re
from jinja2 import Environment, TemplateError
from zool.filter_plugins import filters


def to_list(thing):
    """convert something to a list if necessary"""
    if not isinstance(thing, list):
        return [thing]
    return thing


def template(string, template_vars):
    """template some string with jinja2
    always to and from json so we return an object if it is

    :param string: The template string
    :type: string: str
    :param template_vars: The vars used to render the template
    :type template_vars: dict
    """
    env = Environment(autoescape=True)
    env.filters.update(filters)
    env.policies["json.dumps_kwargs"] = {"sort_keys": False}
    parts = list(string.partition("}}"))
    if not parts[0].strip().endswith("tojson"):
        parts[0] = parts[0] + "|tojson"
    try:
        j_template = env.from_string("".join(parts))
        result = j_template.render(**template_vars)
        result = json.loads(result)
    except TemplateError as exc:
        result = str(exc)
        logging.exception(exc)

    return result


def convert_percentages(dicts, keys, pbar_width):
    """convert a string % to a little progress bar
    not recursive
    80% = 80%|XXXXXXXX  |

    :pararm dicts: a list fo dictionaries
    :type dicts: list of dictionaries
    :param keys: The keys to convert in each dictionary
    :type keys: list of str
    :param pbar_width: The width of the progress bar
    :type pbar_width: int
    """
    for idx, entry in enumerate(dicts):
        for key in [k for k in entry.keys() if k in keys]:
            value = entry[key]
            if re.match(r"^\d{1,3}%$", str(value)):
                numx = int(pbar_width / 100 * int(value[0:-1]) + 0.5)
                entry["_" + key] = value
                entry[key] = "{value} |{numx}|".format(
                    value=value.rjust(4), numx=("X" * numx).ljust(pbar_width)
                )
        dicts[idx] = entry
