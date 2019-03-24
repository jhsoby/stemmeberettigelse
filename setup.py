#!/usr/bin/env python
# encoding=utf-8
from setuptools import setup
import os, sys

setup(
    name='stemmeberettigelse',
      version='1.0.0',
      author='Dan Michael O. Heggø',
      author_email='danmichaelo@gmail.com',
      url='https://github.com/danmichaelo/stemmeberettigelse',
      license='MIT',
      packages=['stemmeberettigelse'],
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
      install_requires=[
        'flask',
        'flup',
        'pytz',
        'PyMySQL',
        'python-dotenv',
      ]
)
