#!/usr/bin/env python
# encoding: utf-8
'''
Created on Oct 15, 2014

@author: tmahrt
'''
import io
from setuptools import setup

setup(name='pysle',
      version='2.1.2',
      author='Tim Mahrt',
      author_email='timmahrt@gmail.com',
      url='https://github.com/timmahrt/pysle',
      package_dir={'pysle':'pysle'},
      packages=['pysle'],
      license='LICENSE',
      description="An interface to ISLEX, an IPA pronunciation dictionary "
                  "for English with stress and syllable markings.",
      long_description=io.open('README.rst', 'r', encoding="utf-8").read()
      )
