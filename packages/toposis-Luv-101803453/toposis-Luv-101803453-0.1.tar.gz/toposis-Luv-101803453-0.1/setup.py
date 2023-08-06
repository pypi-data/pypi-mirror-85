# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 20:34:06 2020

@author: HP
"""

from setuptools import setup

VERSION = '0.1'
PACKAGE_NAME = 'toposis-Luv-101803453'
AUTHOR = 'Luv Gupta'
AUTHOR_EMAIL = 'lgupta1_be18@thapar.edu'

LICENSE = 'Apache License 2.0'

DESCRIPTION = 'TOPSIS is an algorithm to determine the best choice out of many using Positive Ideal Solution and Negative Ideal'

INSTALL_REQUIRES = ['numpy', 'pandas', 'math']

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      install_requires=INSTALL_REQUIRES,
      )