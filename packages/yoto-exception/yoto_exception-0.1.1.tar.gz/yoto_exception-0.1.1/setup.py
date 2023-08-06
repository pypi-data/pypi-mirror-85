#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import importlib

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, "__info__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]

module_name = 'yoto_exception'
mod_info = importlib.import_module(f'{module_name}.__info__')


setup(
    name=module_name,
    version=mod_info.__version__,
    python_requires='>=3.9',
    url=mod_info.__url__,
    description=mod_info.__description__,
    author=mod_info.__author__,
    author_email=mod_info.__email__,
    license="BSD",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=get_packages(module_name),
    package_data={module_name: ["py.typed"]},
    data_files=[("", ["LICENSE.md"])],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
    zip_safe=False,
)
