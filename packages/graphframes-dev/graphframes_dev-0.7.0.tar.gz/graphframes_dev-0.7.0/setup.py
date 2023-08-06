# Your python setup file. An example can be found at:
# https://github.com/pypa/sampleproject/blob/master/setup.py
from setuptools import setup

setup(name='graphframes_dev',
      version='0.7.0',
      packages=['graphframes', 'graphframes.lib', 'graphframes.examples'],
      install_requires=[
          'nose==1.3.3',
          'numpy>=1.7'
      ],
      )