"""
===========
fs.datalake
===========

PythonFileSystem extension for Azure Datalake Store
"""

from setuptools import setup

dev_require = []
setup(
      test_suite='tests.all_tests',
      extras_require={
          'dev': dev_require
      })
