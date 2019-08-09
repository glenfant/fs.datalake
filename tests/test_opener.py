import unittest
from unittest.mock import patch

import fs


class OpenerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.patcher = patch("fs.datalake.DatalakeFS")
        self.MDatalakeFS = self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_with_username_password(self):
        url = "datalake://schtroumpf:secret@storage-name?tenant_id=some-tenant-id"
        storage = fs.open_fs(url)
        self.MDatalakeFS.assert_called_with("storage-name", tenant_id="some-tenant-id", username="schtroumpf",
                                            password="secret")

    def test_with_client_id(self):
        url = "datalake://storage-name?tenant_id=some-tenant-id&client_id=schtroumpf&client_secret=secret"
        storage = fs.open_fs(url)
        self.MDatalakeFS.assert_called_with("storage-name", tenant_id="some-tenant-id", client_id="schtroumpf",
                                            client_secret="secret", username=None, password=None)
