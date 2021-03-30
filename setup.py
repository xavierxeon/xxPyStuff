#!/usr/bin/env python3

import setuptools, platform

def main_apple_silicon():

   with open("README.md", "r") as fh:
      long_description = fh.read()

   packages = setuptools.find_packages()
   packages.remove('xxpystuff.pyside6') # needs pyside6
   packages.remove('xxpystuff.media') # needs numpy and opencv

   setuptools.setup(
      name="xxpystuff",
      version="0.0.8",
      author="Ralf Waspe",
      author_email="rwaspe@me.com",
      description="A collection of python tools",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/xavierxeon/xxPyStuff",
      license='MIT',
      packages=packages,
      install_requires=['colorama'],
      include_package_data=True,
      zip_safe=False,
   )

def main():

   with open("README.md", "r") as fh:
      long_description = fh.read()

   packages = setuptools.find_packages()

   setuptools.setup(
      name="xxpystuff",
      version="0.0.8",
      author="Ralf Waspe",
      author_email="rwaspe@me.com",
      description="A collection of python tools",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/xavierxeon/xxPyStuff",
      license='MIT',
      packages=packages,
      install_requires=['colorama', 'pyside6', 'opencv-python'],
      include_package_data=True,
      zip_safe=False,
   )

if __name__ == '__main__':

   if platform.system() == 'Darwin' and platform.machine() == 'arm64':
      main_apple_silicon()
   else:
      main()
