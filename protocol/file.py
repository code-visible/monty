from typing import TypedDict

SourceFile = TypedDict(
    "SourceFile",
    {
        "id": str,
        "name": str,
        "path": str,
        "pkg": str,
        "deps": list[str],
        "imports": list[str],
    },
)
