# -*- coding: utf-8 -*-
"""Unit tests of fs.adls"""
import os
import unittest

from tests.resources import make_fs


###
# Test layers
###

def setUpModule():
    # Setups for all tests of this module
    return


def tearDownModule():
    # Cleanups for all tests of this module
    return


class ResourceTest(unittest.TestCase):
    """Testing test resources"""

    def test_environment_vars(self):
        """The required environment vars are provided
        """
        self.assertIn("DL_TENANT_ID", os.environ)
        self.assertIn("DL_STORE_NAME", os.environ)
        self.assertIn("DL_CLIENT_ID", os.environ)
        self.assertIn("DL_CLIENT_SECRET", os.environ)
        self.assertIn("DL_USERNAME", os.environ)
        self.assertIn("DL_PASSWORD", os.environ)
        return

    def test_make_fs(self):
        dl_fs = make_fs()
        dummy = 0
