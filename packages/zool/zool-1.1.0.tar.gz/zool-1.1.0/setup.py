""" setup
"""
from setuptools import setup

with open("README.md", "r") as readme:
    LONG_DESCRIPTION = readme.read()

DESCRIPTION = """
A cli for reviewing PRs and zuul's progress
""".strip()

DEPENDENCIES = ["jinja2", "pyyaml", "requests", "pygments", "lxml"]
TEST_DEPENDENCIES = []


VERSION = "1.1.0"
URL = "https://github.com/cidrblock/zool"

setup(
    name="zool",
    version=VERSION,
    author="cidrblock",
    packages=["zool"],
    entry_points={
        "console_scripts": [
            "zool = zool.zool:main",
        ],
    },
    install_requires=DEPENDENCIES,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
)
