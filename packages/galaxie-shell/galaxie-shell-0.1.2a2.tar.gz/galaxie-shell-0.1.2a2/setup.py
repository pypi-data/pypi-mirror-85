#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC APPLICATION_LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Shell Team, all rights reserved

import os
from setuptools import setup
import codecs


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("APPLICATION_VERSION"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


pre_version = get_version("GLXShell/__init__.py")

if os.environ.get("CI_COMMIT_TAG"):
    version = os.environ["CI_COMMIT_TAG"]
else:
    if os.environ.get("CI_JOB_ID"):
        version = os.environ["CI_JOB_ID"]
    else:
        version = pre_version

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="galaxie-shell",
    version=version,
    description="Galaxie Shell is a autonomous shell ready for CI and low tech OS",
    long_description=long_description,
    long_description_content_type="text/x-rst; charset=UTF-8",
    url="https://gitlab.com/aurelien.maury/galaxie-clans-keeper",
    author="Tuuux",
    author_email="tuxa@rtnp.org",
    license="GNU General Public License v3 or later (GPLv3+)",
    packages=["GLXShell",
              "GLXShell.libs",
              "GLXShell.libs.properties",
              "GLXShell.plugins",
              "GLXShell.plugins.builtins",
              ],
    entry_points={"console_scripts": ["glxsh= GLXShell.glxsh:main"]},
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    setup_requires=["green", "wheel", "pyinstaller"],
    tests_require=[
        "wheel",
        "cmd2",
    ],
    install_requires=[
        "wheel",
        "cmd2",
    ],
)
