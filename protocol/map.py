from typing import TypedDict

from .abstract import SourceAbstract
from .call import SourceCall
from .callable import SourceCallable
from .dep import SourceDep
from .file import SourceFile
from .pkg import SourcePkg
from .reference import SourceReference

Source = TypedDict(
    "Source",
    {
        "name": str,
        "lang": str,
        "parser": str,
        "protocol": str,
        "timestamp": str,
        "typ": str,
        "repository": str,
        "version": str,
        "pkgs": list[SourcePkg],
        "files": list[SourceFile],
        "absts": list[SourceAbstract],
        "fns": list[SourceCallable],
        "calls": list[SourceCall],
        "refs": list[SourceReference],
        "deps": list[SourceDep],
    },
)
