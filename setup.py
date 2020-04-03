#!/usr/bin/env python3

from setuptools import setup
from matrixdemos import __version__

setup(
    version=__version__,
    package_data = {"matrixdemos" : ["fonts/*", "demo_slideshow/*", "animations/*/*"]},
    python_requires=">=3.6",
)
