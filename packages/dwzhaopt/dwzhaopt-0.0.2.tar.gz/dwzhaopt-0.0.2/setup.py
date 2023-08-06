#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def read(f_name):
    return open(os.path.join(os.path.dirname(__file__), f_name)).read()


setup(
    name="dwzhaopt",
    version="0.0.2",
    author="dwzhao",
    author_email="flybx@foxmail.com",
    description="An demonstration of how to create, test, document and publish to pypi.org.",
    license='MIT License',
    keywords="pip test document tutorial",
    url="https://github.com/betterzdw/dwzhaopt",
    packages=find_packages(),
    long_description=read('README.md'),

    entry_points={
        'console_scripts': [
            'dwzhaopt = dwzhaopt.echo:echo',
        ],
    },
)
