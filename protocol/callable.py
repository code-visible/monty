from typing import TypedDict

SourceCallable = TypedDict(
    "SourceCallable",
    {
        "id": str,
        "pos": str,
        "name": str,
        "signature": str,
        "abstract": str,
        "file": str,
        "pkg": str,
        "comment": str,
        "parameters": list[str],
        "results": list[str],
        "method": bool,
        "private": bool,
        "orphan": bool,
    },
)
