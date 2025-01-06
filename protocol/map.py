from typing import TypedDict
from .abstract import SourceAbstract
from .call import SourceCall
from .callable import SourceCallable
from .dep import SourceDep
from .file import SourceFile
from .pkg import SourcePkg

Source = TypedDict(
    "Source",
    {
        "name": str,
        "directory": str,
        "language": str,
        "pkgs": list[SourcePkg],
        "files": list[SourceFile],
        "abstracts": list[SourceAbstract],
        "callables": list[SourceCallable],
        "calls": list[SourceCall],
        "deps": list[SourceDep],
    },
)
