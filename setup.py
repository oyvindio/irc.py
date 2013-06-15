#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='irc.py',
      version='0.1',
      description='Super thin irc abstraction over asynchat',
      author='Øyvind Ingebrigsen Øvergaard',
      author_email='oyvind.overgaard@gmail.com',
      packages=['irc'],
      test_suite='nose.collector',
      tests_require='nose>=1.3.0'
      )
