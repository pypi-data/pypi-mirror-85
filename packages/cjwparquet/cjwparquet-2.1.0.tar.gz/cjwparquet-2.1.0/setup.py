#!/usr/bin/env python3

import sys
from os.path import dirname, join

from setuptools import find_packages, setup

# We use the README as the long_description
readme = open(join(dirname(__file__), "README.md")).read()

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)

setup(
    name="cjwparquet",
    version="2.1.0",
    url="http://github.com/CJWorkbench/cjwparquet/",
    author="Adam Hooper",
    author_email="adam@adamhooper.com",
    description="Utilities to help build Workbench modules",
    include_package_data=True,
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    zip_safe=True,
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["pyarrow>=1.0, <3.0"],
    setup_requires=["pytest-runner~=6.0"] if needs_pytest else [],
    extras_require={"tests": ["pytest~=6.0", "pytz"]},
)
