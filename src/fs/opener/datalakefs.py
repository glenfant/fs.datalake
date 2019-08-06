# Typings
from typing import Text
from urllib.parse import ParseResult

from fs.base import FS
from fs.datalake import DatalakeFS
from fs.opener.base import Opener
# from fs.opener.errors import OpenerError
from fs.opener.registry import registry


class DatalakeOpener(Opener):
    protocols = ["datalake"]

    def open_fs(
            self,
            fs_url,  # type: Text
            parse_result,  # type: ParseResult
            writeable,  # type: bool
            create,  # type: bool
            cwd,  # type: Text
    ):  # type: (...) -> FS
        username = parse_result.username
        password = parse_result.password
        tenant_id, store_name = parse_result.resource.split("/")
        client_id = parse_result.params.get("client_id")
        client_secret = parse_result.params.get("client_secret")
        return DatalakeFS(tenant_id, store_name, username=username, password=password, client_id=client_id,
                          client_secret=client_secret)


registry.install(DatalakeOpener)
