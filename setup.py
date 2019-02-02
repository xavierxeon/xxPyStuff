#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()

setuptools.setup(
    name="xxpystuff",
    version="0.0.7",
    author="Ralf Waspe",
    author_email="rwaspe@me.com",
    description="A collection of python tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xavierxeon/xxPyStuff",
    license='MIT',
    packages=packages,
    install_requires=['colorama', 'pyside2', 'urwid'],
    include_package_data=True,
    zip_safe=False,
)