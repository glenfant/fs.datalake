from abc import ABC

from fs.opener.base import Opener
from fs.opener.errors import OpenerError
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
        from fs.datalake import DatalakeFS
        import pdb; pdb.set_trace()
        return


registry.install(DatalakeOpener)
