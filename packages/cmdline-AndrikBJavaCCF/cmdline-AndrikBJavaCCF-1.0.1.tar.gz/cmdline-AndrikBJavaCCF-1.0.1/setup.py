# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re

from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('AndrikBJavaCCF/main.py').read(),
    re.M
).group(1)

with open("README.rst", "r", encoding='utf-8') as f:
    long_descr = f.read()

setup(
    name="cmdline-AndrikBJavaCCF",
    packages=["AndrikBJavaCCF"],
    entry_points={
        "console_scripts": ['AndrikBJavaCCF = AndrikBJavaCCF.main:main']
    },
    version=version,
    description="Python command line application to fix java code convention.",
    long_description=long_descr,
    author="Andrii Blahyi",
    author_email="blagij00@gmail.com",
    url="https://github.com/AndrikB",
)
