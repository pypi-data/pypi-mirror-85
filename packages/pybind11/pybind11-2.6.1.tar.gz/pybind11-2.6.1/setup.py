#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Setup script (in the sdist or in tools/setup_main.py in the repository)

from setuptools import setup

cmdclass = {}


setup(
    name="pybind11",
    version="2.6.1",
    download_url='https://github.com/pybind/pybind11/tarball/v2.6.1',
    packages=[
        "pybind11",
        "pybind11.include.pybind11",
        "pybind11.include.pybind11.detail",
        "pybind11.share.cmake.pybind11",
    ],
    package_data={
        "pybind11": ["py.typed", "*.pyi"],
        "pybind11.include.pybind11": ["*.h"],
        "pybind11.include.pybind11.detail": ["*.h"],
        "pybind11.share.cmake.pybind11": ["*.cmake"],
    },
    extras_require={
        "global": ["pybind11_global==2.6.1"]
        },
    entry_points={
        "console_scripts": [
             "pybind11-config = pybind11.__main__:main",
        ]
    },
    cmdclass=cmdclass
)
