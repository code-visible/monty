from typing import TypedDict

SourceCall = TypedDict(
    "SourceCall",
    {
        "id": str,
        "pos": str,
        "caller": str,
        "callee": str,
        "file": str,
        "type": str,
    },
)
