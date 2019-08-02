# -*- coding: utf-8 -*-
"""\
=======
fs.adls
=======

Tests package
"""
import unittest

from .resources import tests_directory

def all_tests():
    return unittest.defaultTestLoader.discover(tests_directory)
