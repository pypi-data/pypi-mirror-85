import os
from setuptools import setup

version = os.environ.get('PACKAGE_VERSION')

setup(
    version=version,
)
