"""
======================
ds.datalake.filesystem
======================

See https://docs.pyfilesystem.org/en/latest/implementers.html#
"""
from datetime import datetime, timedelta
import logging
from typing import Text, Optional, Collection, Dict, List, Any, BinaryIO, Mapping

from fs.base import FS
from fs.info import Info, Permissions
from fs.enums import ResourceType
from fs.subfs import SubFS
from azure.datalake.store import core as datalake_core, lib as datalake_lib

RawInfo = Mapping[Text, Mapping[Text, object]]

LOG = logging.getLogger(__name__)


class DatalakeFS(FS):
    # See https://docs.pyfilesystem.org/en/latest/reference/base.html#fs.base.FS.getmeta
    _meta = {
        "standard": {
            "case_insensitive": False,
            "invalid_path_chars": "",
            "max_path_length": None,
            "max_sys_path_length": None,
            "network": True,
            "read_only": False,
            "supports_rename": True
        }
    }

    def __init__(self, store_name: Text, **auth_kwargs):
        """
        Args:
            store_name: Name of the Datalake store
            auth_kwargs: Keyword arguments required to authenticate in azure.datalake.store.lib.auth

        Please read and understand the complicated Datalake authentication logic
        """
        # Warning, the token is valid for one hour.
        token = datalake_lib.auth(**auth_kwargs)
        self.datalake = datalake_core.AzureDLFileSystem(token, store_name=store_name)
        super().__init__()

    # Essential methods https://docs.pyfilesystem.org/en/latest/implementers.html#essential-methods

    def getinfo(self, path: Text, namespaces: Optional[Collection[Text]] = None) -> Info:
        """See https://docs.pyfilesystem.org/en/latest/info.html#info-objects
        """
        LOG.debug(f"getinfo({path})")
        namespaces = namespaces or ()
        dl_info = self.datalake.info(path)
        # Info for a directory:
        # {'length': 0, 'pathSuffix': '', 'type': 'DIRECTORY', 'blockSize': 0, 'accessTime': 1538409759284,
        # 'modificationTime': 1538410080090, 'replication': 0, 'permission': '770',
        # 'owner': '8886da14-6bc6-4464-b927-3b6bfd72a0a8', 'group': '4e72d379-c168-4393-883e-0221806f96e9',
        # 'aclBit': False, 'name': 'billy/billy_int/TEST_PROVIDER'}
        # Info for a file
        # {'length': 100664, 'pathSuffix': '', 'type': 'FILE', 'blockSize': 268435456, 'accessTime': 1538410067444,
        # 'modificationTime': 1538410067491, 'replication': 1, 'permission': '770',
        # 'owner': '8886da14-6bc6-4464-b927-3b6bfd72a0a8', 'group': '4e72d379-c168-4393-883e-0221806f96e9',
        # 'msExpirationTime': 0, 'aclBit': False,
        # 'name': 'billy/billy_int/TEST_PROVIDER/EDF_8907832648_10031876816_10112015.pdf'}
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
            # Expecting reply to https://github.com/Azure/azure-data-lake-store-python/issues/296
            # about Datalake timestamps
            raw_info["details"] = {
                "accessed": dl_info["accessTime"] / 1000.0,
                "modified": dl_info["modificationTime"] / 1000.0,
                "size": dl_info["length"],
                "type": details_type,
                # Not provided by Datalake API
                "metadata_changed": None,
                "created": None
            }
        if "access" in namespaces:
            int_permissions = int(dl_info["permission"], base=8)
            permissions = Permissions.create(int_permissions)
            raw_info["access"] = {
                "group": dl_info["group"],
                "user": dl_info["owner"],
                "permissions": permissions.dump()
            }

        return Info(raw_info)

    def listdir(self, path: Text) -> List[Text]:
        LOG.debug(f"listdir({path})")
        results = self.datalake.ls(path)
        return [result.rsplit("/", 1)[-1] for result in results]

    def makedir(self, path: Text, permissions: Optional[Permissions] = None, recreate: bool = False) -> SubFS[FS]:
        LOG.debug(f"makedir({path})")
        return

    def openbin(self, path: Text, mode: Text = "r", buffering: int = -1, **options) -> BinaryIO:
        LOG.debug(f"openbin({path})")
        return

    def remove(self, path: Text) -> None:
        LOG.debug(f"remove({path})")
        return

    def removedir(self, path: Text) -> None:
        LOG.debug(f"removedir({path})")
        return

    def setinfo(self, path: Text, info: RawInfo) -> None:
        LOG.debug(f"setinfo({path})")
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
