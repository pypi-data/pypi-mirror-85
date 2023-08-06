#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "fsociety"
DESCRIPTION = "A Modular Penetration Testing Framework"
URL = "https://fsociety.dev/"
PROJECT_URLS = {
    "Packages": "https://github.com/fsociety-team/fsociety/blob/master/PACKAGES.md",
    "Changelog": "https://github.com/fsociety-team/fsociety/blob/master/CHANGELOG.md",
    "Funding": "https://github.com/sponsors/thehappydinoa",
    "Tracker": "https://github.com/fsociety-team/fsociety/issues",
    "Source": "https://github.com/fsociety-team/fsociety",
}
EMAIL = "contact@fsociety.dev"
AUTHOR = "fsociety-team"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = None

# Required Packages
REQUIRED = ["gitpython", "rich>=9.2.0", "requests"]

# Optional Packages
EXTRAS = {"dev": ["wheel", "pylint", "autopep8", "twine", "mypy", "flake8"]}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class TagCommand(Command):
    """Support setup.py push_tag."""

    description = "Push latest version as tag."
    user_options = []

    @staticmethod
    def status(s):
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    project_urls=PROJECT_URLS,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    entry_points={"console_scripts": ["fsociety=fsociety:cli"],},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    # python setup.py upload
    cmdclass={"push_tag": TagCommand},
)
