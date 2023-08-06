import os
from setuptools import setup # type: ignore

version = os.environ.get('PACKAGE_VERSION')

setup(
    version=version,
)
