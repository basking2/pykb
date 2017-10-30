#!/usr/bin/env python

from setuptools import setup

setup(name='pykb',
      version='0.0.1',
      description='Python Knowledge Base \'n Stuff',
      url='https://github.com/basking2/pykb',
      author='Sam Baskinger',
      author_email='samuel.baskinger@yahoo.com',
      license='MIT',
      packages=['pykb'],
      scripts=[
          ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
