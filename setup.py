#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wapy",
    version="0.0.6",
    author="Ralf Waspe",
    author_email="rwaspe@me.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xavierxeon/PythonPackage",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['colorama', 'pyside2', 'urwid'],
    include_package_data=True,
    zip_safe=False,
)