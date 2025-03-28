from typing import TypedDict

SourceReference = TypedDict(
    "SourceReference",
    {
        "id": str,
        "pos": str,
        "file": str,
    },
)
