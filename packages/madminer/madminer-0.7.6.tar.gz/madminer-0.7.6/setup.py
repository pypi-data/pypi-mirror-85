#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on https://github.com/kennethreitz/setup.py

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command


project_dir = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with open(os.path.join(project_dir, 'README.md')) as f:
    LONG_DESCRIPTION = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
info = {}
with open(os.path.join(project_dir, 'madminer', '__info__.py')) as f:
    exec(f.read(), info)


# Package meta-data.
NAME = 'madminer'
DESCRIPTION = 'Mining gold from MadGraph to improve limit setting in particle physics.'
URL = 'https://github.com/diana-hep/madminer'
EMAIL = 'johann.brehmer@nyu.edu'
REQUIRES_PYTHON = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4'
AUTHORS = info['__authors__']
VERSION = info['__version__']
REQUIRED = [
    "future",
    "h5py",
    "matplotlib>=2.0.0",
    "numpy>=1.13.0",
    "scipy>=1.0.0",
    "scikit-hep>=0.5.0, <0.6.0",
    "six",
    "torch>=1.0.0",
    "uproot",
]

EXTRAS_DOCS = sorted(
    [
        "numpydoc",
        "recommonmark",
        "sphinx>=1.4",
        "sphinx_rtd_theme",
    ]
)
EXTRAS_TEST = sorted(
    EXTRAS_DOCS + [
        "pytest",
    ]
)
EXTRAS_EXAMPLES = sorted(
    [
        "bqplot",
        "pandas",
    ]
)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(project_dir, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHORS,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    extras_require={
        "docs": EXTRAS_DOCS,
        "test": EXTRAS_TEST,
        "examples": EXTRAS_EXAMPLES,
    },
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
