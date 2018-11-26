#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="wapy",
    version="0.0.5",
    author="Ralf Waspe",
    author_email="ralf@waspe.de",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['colorama', 'pyside2'],
    include_package_data=True,
    zip_safe=False,
)