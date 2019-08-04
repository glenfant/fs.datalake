"""
======================
ds.datalake.filesystem
======================

See https://docs.pyfilesystem.org/en/latest/implementers.html#
"""

from typing import Text, Optional, Collection, List, Any, BinaryIO, Mapping

from fs.base import FS
from fs.info import Info, Permissions
from fs.subfs import SubFS
from azure.datalake.store import core as datalake_core, lib as datalake_lib

RawInfo = Mapping[Text, Mapping[Text, object]]


class DatalakeFS(FS):
    def __init__(self, tenant_id, username, password, store_name):
        token = datalake_lib.auth(tenant_id, username, password)
        self.datalake = datalake_core.AzureDLFileSystem(token, store_name=store_name)
        super().__init__()

    # Mandatory methods

    def getinfo(self, path, namespaces=None):  # type: (Text, Optional[Collection[Text]]) -> Info
        info = self.datalake.info(path)
        return Info()

    def listdir(self, path):  # type: (Text) -> List[Text]
        return

    def makedir(
            self,
            path,  # type: Text
            permissions=None,  # type: Optional[Permissions]
            recreate=False,  # type: bool
    ):  # type: (...) -> SubFS[FS]
        return

    def openbin(
            self,
            path,  # type: Text
            mode="r",  # type: Text
            buffering=-1,  # type: int
            **options  # type: Any
    ):  # type: (...) -> BinaryIO
        return

    def remove(self, path):  # type: (Text) -> None
        return

    def removedir(self, path):  # type: (Text) -> None
        return

    def setinfo(self, path, info):  # type: (Text, RawInfo) -> None
        return
