"""
======================
ds.datalake.filesystem
======================

See https://docs.pyfilesystem.org/en/latest/implementers.html#
"""

from fs.base import FS, SubFS, BinaryIO

from fs.info import Info, Permissions, RawInfo

from typing import Text, Optional, Collection, List, Any


class DatalakeFS(FS):
    def __init__(self):
        super().__init__()

    # Mandatory methods

    def getinfo(self, path, namespaces=None):  # type: (Text, Optional[Collection[Text]]) -> Info
        return

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
