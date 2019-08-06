"""
======================
ds.datalake.filesystem
======================

See https://docs.pyfilesystem.org/en/latest/implementers.html#
"""

from typing import Text, Optional, Collection, List, Any, BinaryIO, Mapping

from fs.base import FS
from fs.info import Info, Permissions
from fs.enums import ResourceType
from fs.subfs import SubFS
from azure.datalake.store import core as datalake_core, lib as datalake_lib

RawInfo = Mapping[Text, Mapping[Text, object]]


class DatalakeFS(FS):
    # See https://docs.pyfilesystem.org/en/latest/reference/base.html#fs.base.FS.getmeta
    _meta = {
        "standard": {
            "case_insensitive": True,
            "invalid_path_chars": "",
            "max_path_length": None,
            "max_sys_path_length": None,
            "network": True,
            "read_only": False,
            "supports_rename": True
        }
    }

    def __init__(self, tenant_id: Text, store_name: Text, username: Text = None, password: Text = None,
                 client_id: Text = None, client_secret: Text = None):
        """
        You should not provide both ``username`` / ``password`` params or ``client_id`` / ``client_secret``
        params but not both.

        Please read the Azure Datalake documentation about these parameters.

        Args:
            tenant_id: Provided by your Azure dashboard
            store_name: Name of the Datalake store
            username: Azure credentials
            password: Azure credentials
            client_id: Token
            client_secret:
        """
        # Checking parameters
        assert username or client_id, "You must provide one of 'username' or 'client_id' kw args"
        assert (username and client_id) is None, "You should not provide 'username' and 'client_id' kw args"
        if username:
            assert isinstance(password, str) and len(password), "You must provide 'password' kw arg"
        else:
            assert isinstance(client_secret, str) and len(client_secret), "You must provide 'client_secret' kw arg"

        # Warning, the token is valid for one hour.
        token = datalake_lib.auth(tenant_id=tenant_id, username=username, password=password, client_id=client_id,
                                  client_secret=client_secret)
        self.datalake = datalake_core.AzureDLFileSystem(token, store_name=store_name)
        super().__init__()

    # Mandatory methods

    def getinfo(self, path, namespaces=None):  # type: (Text, Optional[Collection[Text]]) -> Info
        """See https://docs.pyfilesystem.org/en/latest/info.html#info-objects
        """
        namespaces = namespaces or ()
        dl_info = self.datalake.info(path)
        # Info for a directory:
        # {'length': 0, 'pathSuffix': '', 'type': 'DIRECTORY', 'blockSize': 0, 'accessTime': 1538409759284, 'modificationTime': 1538410080090, 'replication': 0, 'permission': '770', 'owner': '8886da14-6bc6-4464-b927-3b6bfd72a0a8', 'group': '4e72d379-c168-4393-883e-0221806f96e9', 'aclBit': False, 'name': 'billy/billy_int/TEST_PROVIDER'}
        # Info for a file
        # {'length': 100664, 'pathSuffix': '', 'type': 'FILE', 'blockSize': 268435456, 'accessTime': 1538410067444, 'modificationTime': 1538410067491, 'replication': 1, 'permission': '770', 'owner': '8886da14-6bc6-4464-b927-3b6bfd72a0a8', 'group': '4e72d379-c168-4393-883e-0221806f96e9', 'msExpirationTime': 0, 'aclBit': False, 'name': 'billy/billy_int/TEST_PROVIDER/EDF_8907832648_10031876816_10112015.pdf'}
        dl_info_type = dl_info["type"]
        if dl_info_type == "DIRECTORY":
            is_directory = True
            details_type = ResourceType.directory
        elif dl_info_type == "FILE":
            is_directory = False
            details_type = ResourceType.file
        else:
            is_directory = False
            details_type = ResourceType.unknown

        raw_info = {
            "basic":
                {"name": dl_info["name"].rsplit("/", 1)[-1],
                 "is_dir": is_directory
                 }
        }
        if "details" in namespaces:
            raw_info["details"] = {
                "accessed": dl_info["accessTime"],
                "modified": dl_info["modificationTime"],
                "size": dl_info["length"],
                "type": details_type
            }
        if "access" in namespaces:
            raw_info["access"] = {
                "group": dl_info["group"],
                "user": dl_info["user"],
                "permissions": raw_permissions(dl_info["permission"])
            }

        return Info(raw_info)

    def listdir(self, path):  # type: (Text) -> List[Text]
        results = self.datalake.ls(path)
        return [result.rsplit("/", 1)[-1] for result in results]

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


def raw_permissions(octal_perms: str) -> List[Text]:
    """Makes a list of permissions as expected for raw info
    from an octal permission in a string.
    See https://docs.pyfilesystem.org/en/latest/info.html#raw-info
    """
    bit_perms = int(octal_perms, base=8)
    # From bit 0 to 8
    perm_names = ["o_x", "o_w", "o_r", "g_x", "g_w", "g_r", "u_x", "u_w", "u_r"]
    resource_perms = []
    mask = 1
    for name in perm_names:
        if bit_perms & mask == mask:
            resource_perms.append(name)
        mask <<= 1
    return resource_perms
