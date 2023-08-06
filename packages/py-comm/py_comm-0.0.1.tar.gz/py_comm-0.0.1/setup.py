# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from py_comm import __version__

name = "py_comm"
setup(
    name=name,
    version=__version__,
    keywords=["pip", "commons", "common", "utils", "util"],
    description="Common utils for python",
    packages=find_packages(include=[name, f"{name}.*"], exclude=["test", "test.*"]),
    include_package_data=True,
    platforms="any"
)
