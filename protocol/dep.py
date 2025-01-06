from typing import TypedDict

SourceDep = TypedDict(
    "SourceDep",
    {
        "id": str,
        "name": str,
        "type": str,
        "ref": str,
    },
)
