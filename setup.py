#!/usr/bin/env python3
import os
from setuptools import setup
from matrixdemos import __version__

setup(
    version=__version__,
    package_data = {"matrixdemos" : ["fonts/*", "demo_slideshow/*", "" if "NOANIMATION" in os.environ else "animations/*/*", "images/*"]},
    python_requires=">=3.6",
)
