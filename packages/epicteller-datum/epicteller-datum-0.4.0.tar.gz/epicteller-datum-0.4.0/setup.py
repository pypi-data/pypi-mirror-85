#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'lark-parser>=0.7.1',
]

setup_requirements = []

test_requirements = [
    'coverage',
    'pytest',
    'pytest-cov',
    'pytest-flakes',
    'pytest-pep8',
]

setup(
    author="Kawashiro Nitori",
    author_email='nitori@ikazuchi.cn',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Dice parser for Epicteller.",
    entry_points={},
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='datum',
    name='epicteller-datum',
    packages=find_packages(include=['datum']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/epicteller/datum',
    version='0.4.0',
    zip_safe=False,
)
