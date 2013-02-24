#!/usr/bin/env python
# vim: set fileencoding=utf-8 sw=4 ts=4 et :
from setuptools import setup

from distutils.core import setup

setup(name='pylogic',
      version='1.0.0',
      description='Python Module for Logical Validation',
      author='Rob Truxler',
      author_email='rtruxler [ at ] gmail.com',
      license='LGP:',
      url='',
      install_requires=[
          "setuptools",
          ],
      packages = ['pylogic',],
      package_dir = {'': 'src'},
      namespace_packages = ['pylogic', ],
     )
