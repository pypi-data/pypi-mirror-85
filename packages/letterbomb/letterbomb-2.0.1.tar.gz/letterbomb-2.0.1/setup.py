#!/usr/bin/env python3
# coding=utf-8
"""
Setup.py for Letterbomb.

For usage with `pip install`.
See ``README.md`` for instructions.
"""
from setuptools import setup, find_packages

import letterbomb

try:
    with open("README.md") as f:
        long_description: str = f.read()
except OSError:
    long_description: str = 'Unable to read "README.md"'
    print(long_description)

setup(
    name=letterbomb.__project__.lower(),
    version=letterbomb.__version__,
    author=letterbomb.__author__,
    author_email="4616947-whoatemybutter@users.noreply.gitlab.com",
    maintainer=letterbomb.__author__,
    maintainer_email="4616947-whoatemybutter@users.noreply.gitlab.com",
    url=letterbomb.__url__,
    description="A fork of the classic Wii hacking tool from fail0verflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
    download_url=letterbomb.__download__,
    license="GPLv3+",
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Games/Entertainment"
    ],
    python_requires=">=3.6"
)
