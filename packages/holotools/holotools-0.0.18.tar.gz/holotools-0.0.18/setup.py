#!/usr/bin/env python3

from setuptools import setup,find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
name='holotools', #pypi name
version = '0.0.18',
description='Python Code Base Used by the Holobiome Team',
py_modules=['biom'
            'barrnap',
            ], #'import' name
packages=['holotools'],
long_description=long_description,
long_description_content_type="text/markdown",
install_requires=["pandas"],
extras_require={"dev":["pytest>=3.6",]},
url = "https://github.com/HolobiomeProject/holotools", #sdist
author="Barry Guglielmo",
author_email="barryguglielmo@gmail.com"
)
