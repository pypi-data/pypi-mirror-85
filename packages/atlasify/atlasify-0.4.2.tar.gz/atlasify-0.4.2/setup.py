"""
This script is used to install atlasify and all its dependencies. Run

    python setup.py install
or
    python3 setup.py install

to install the package.
"""

# Copyright (C) 2019-2020 Frank Sauerburger

from setuptools import setup

def load_long_description(filename):
    """
    Loads the given file and returns its content.
    """
    with open(filename) as readme_file:
        content = readme_file.read()
        return content

setup(name='atlasify',
      version='0.4.2',  # Also change in module
      packages=["atlasify", "atlasify.tests"],
      package_data={'atlasify': ['fonts/*.ttf']},
      install_requires=["matplotlib", "packaging"],  # Also add in requirements.txt
      test_suite='atlasify.tests',
      description="Applies ATLAS style to matplotlib plots",  # Short description
      long_description=load_long_description("README.md"),
      long_description_content_type='text/markdown',
      url="https://gitlab.cern.ch/fsauerbu/atlasify",
      author="Frank Sauerburger",
      author_email="f.sauerburger@cern.ch",
      classifiers=["Intended Audience :: Science/Research",
                   "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8",
                   "Topic :: Scientific/Engineering :: Physics"],
      license="AGPL-3.0")
