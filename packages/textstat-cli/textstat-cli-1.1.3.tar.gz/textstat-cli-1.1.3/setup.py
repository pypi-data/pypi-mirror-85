#!/usr/bin/env python

from distutils.core import setup

import textstat_cli

setup(
    name="textstat-cli",
    version=textstat_cli.__version__,
    description="A CLI wrapper for the textstat library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Matt Copperwaite",
    author_email="matt@copperwaite.net",
    url="https://github.com/yamatt/python3-textstat-cli",
    packages=["textstat_cli"],
    install_requires=open("requirements.txt", encoding="utf-8").readlines(),
    scripts=["scripts/textstat"],
    license="gplv3",
    project_urls={
        "Source": "https://github.com/yamatt/python3-textstat-cli",
        "Tracker": "https://github.com/yamatt/python3-textstat-cli/issues",
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
