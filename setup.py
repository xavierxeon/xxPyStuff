#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="wapy",
    version="0.0.1",
    author="Ralf Waspe",
    author_email="ralf@waspe.de",
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
)