#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess
import bundesliga

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    subprocess.call(['python', 'setup.py', 'sdist', 'upload', '--sign'])
    sys.exit()

README = open('README.md').read()
LICENSE = open("LICENSE").read()

setup(
    name='bundesliga-cli',
    version=bundesliga.__version__,
    description='JiraCards prints agile cards for your physical board from Jira. The issues are read from a Jira Agile Board or individual issues can be provided to create single cards.',
    long_description=(README),
    author='Sebastian Ruml',
    author_email='sebastian@sebastianruml.name',
    url='https://github.com/hypebeast/bundesliga-cli',
    include_package_data=True,
    install_requires=[
        'click >= 3.3.0',
        'prettytable >= 0.7.2'
    ],
    license=(LICENSE),
    keywords='python, cli, bundesliga, germany',
    packages=['bundesliga'],
    scripts=['bin/buli']
)
