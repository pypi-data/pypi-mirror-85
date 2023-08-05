#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pkgver import package_version
with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'click>=6.0',
    'twine',
    'boto3',
    'PyYAML==5.3.1',
    'docker'
]

setup(
    name='scora-cli',
    version=package_version,
    description="Scora Platform CLI",
    long_description=readme,
    author="Oncase",
    author_email='contato@oncase.com.br',
    url='https://pypi.org/project/scora/',
    packages=find_packages(include=['pkgver', 'pkgver.*', 'scora', 'scora.*']),
    entry_points={
        'console_scripts': [
            'scora=scora:cli'
        ]
    },
    include_package_data=True,
    zip_safe=True,
    install_requires=requirements,
    extras_require={
        'dev': [
            'twine>=3.1.1',
            'Sphinx==3.1.1',
            'sphinxcontrib-napoleon==0.7',
            'sphinx-rtd-theme==0.5.0',
            'sphinx-click==2.3.2',
            'flake8==3.8.3'
        ]
    },
    keywords='scora',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ]
)
