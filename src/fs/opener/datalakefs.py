# Typings
from typing import Text

from fs.base import FS
from fs.datalake import DatalakeFS
from fs.opener.base import Opener
from fs.opener.parse import ParseResult
# from fs.opener.errors import OpenerError
from fs.opener.registry import registry


class DatalakeOpener(Opener):
    protocols = ["datalake"]

    def open_fs(self, fs_url: Text, parse_result: ParseResult, writeable: bool, create: bool,
                cwd: Text) -> FS:
        username = parse_result.username
        password = parse_result.password
        store_name = parse_result.resource
        return DatalakeFS(store_name, username=username, password=password, **parse_result.params)


registry.install(DatalakeOpener)
