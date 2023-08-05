#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

setup(
    name='booknot',
    version='0.0.7',
    packages=find_packages(exclude=["*_tests"]),
    license='MIT license',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={
        'configuration': ['booknot/resources/*', 'booknot/resources/booknot_root/*'],
    },
    entry_points = {
        'console_scripts': [
            'booknot = booknot.cli:cli',
        ],
    },
    install_requires = [
        'attrs',
        'beautifulsoup4',
        'click',
        'decorator',
        'inquirer',
        'jinja2',
        'plumbum',
        'requests',
        'sphinx'
    ],
    extras_require={
        'dev': [
            'pylint',
            'coverage',
            'tox',
            'twine'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Environment :: Console"
    ]
)
