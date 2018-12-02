#!/usr/bin/env python

import io
import os

from setuptools import find_packages, setup

from _version import __version__

REQUIRED = [
    'flask',
    'sqlalchemy',
    'toml'
]

EXTRAS = {
}

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='frangiclave-compendium',
    version=__version__,
    description='A tool for viewing Cultist Simulator data.',
    long_description=long_description,
    author='Lyrositor',
    python_requires='>=3.6.0',
    url='https://github.com/frangiclave/frangiclave-compendium',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'flask',
        'sqlalchemy',
        'toml',
        'uwsgi'
    ],
    extras_require={},
    include_package_data=True,
    license='CC0'
)
