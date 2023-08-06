#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages #Import setuptools utils

import pylivereloader #Import main script

setup(
    name = "pylivereloader", #Package name
    version = pylivereloader.__version__, #Package version
    packages = find_packages(), #Find packages needed by core
    author = "Z3R0xLEGEND", #Author name
    author_email = "legend.z3r00.pro@gmail.com", #Mail contact
    description = "Script live reloader for production environment", #Package description
    long_description = open("README.rst").read(), #File description
    url = "http://github.com/Z3R0xLEGEND/pylivereloader", #Official support page
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
    ], #Package metadata for pypi
    license = "MIT", #Package license
    platforms = "ALL" #Package platforms
) #Setup the main
