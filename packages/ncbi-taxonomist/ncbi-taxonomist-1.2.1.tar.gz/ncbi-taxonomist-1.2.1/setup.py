# Adapted from numpy:
# https://github.com/numpy/numpy/blob/master/setup.py

import os
import sys
import setuptools


fh = open('src/ncbitaxonomist/VERSION.pypi', 'r')
ver = fh.readline().strip()
fh.close()

setuptools.setup(version=ver)
