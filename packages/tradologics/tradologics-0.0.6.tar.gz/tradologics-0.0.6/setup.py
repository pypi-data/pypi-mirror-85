#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = "0.0.6"


def get_requirements():
    with open("requirements.txt") as f:
        return [line.rstrip() for line in f]


def get_description():
    with open("README.rst") as f:
        return f.read()


setup(
    name="tradologics",
    version=VERSION,
    description="Tradologics SDK",
    long_description=get_description(),
    url="https://tradologics.com",
    author="Tradologics, Inc.",
    author_email="opensource@tradologics.com",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",

        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",

        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    platforms=["any"],
    keywords="tradologics, tradologics.com",
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=get_requirements()
)
