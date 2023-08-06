#!/usr/bin/env python3

import os
import re

from setuptools import setup, find_packages


base_dir = os.path.dirname(__file__)
pkg_name = "ak47"


about = {}
with open(os.path.join(base_dir, pkg_name, "__about__.py")) as file_handler:
    exec(file_handler.read(), about)

with open(os.path.join(base_dir, "README.rst")) as file_handler:
    long_description = file_handler.read()

with open(os.path.join(base_dir, "CHANGES.rst")) as file_handler:
    changelog = re.sub(
        r":issue:`(\d+)`",
        r"`#\1 <https://github.com/pypa/packaging/issues/\1>`__",
        file_handler.read(),
    )
    long_description = "\n".join([long_description, changelog])

def get_all_pkgs(path='pkgs'):
    pkgs_list = []
    _path = os.path.join(os.path.dirname(__file__), path)
    for item in os.listdir(_path):
        pkgs_list.append(path + "/" + item)
    return pkgs_list


setup(
    name=about["__title__"],
    version=about["__version__"],
    packages=find_packages() + get_all_pkgs(),
    scripts = ['ak47/_installer.py'],

    install_requires=[
        "setuptools",
        "PyYAML",
        "mock",
        "coverage"
    ],
    # package_data={"ak47": [""]},

    author=about["__author__"],
    author_email=about["__email__"],
    description=about["__summary__"],
    long_description=long_description,
    license=about["__license__"],
    keywords = "plucky",
    url=about["__uri__"],

    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)