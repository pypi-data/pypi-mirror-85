#!/usr/bin/env python3

import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license=about["__license__"],
    url=about["__uri__"],
    author=about["__author__"],
    author_email=about["__email__"],
    python_requires=">=3.7",
    # install_requires=["twine"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=["ak47"],
    package_data={"ak47": ["py.typed"]},
)