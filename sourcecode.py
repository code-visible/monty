from utils import caculate_hash_id  # type: ignore
import os

from protocol.pkg import SourcePkg
from protocol.dep import SourceDep
from protocol.file import SourceFile


class Dir:
    """Class representing a directory"""

    id: str
    path: str
    files: int
    pkg: bool

    def __init__(self, path: str):
        self.id = caculate_hash_id(path)
        self.path = path
        self.files = 0
        self.pkg = False

    def dump(self) -> SourcePkg:
        return {
            "id": self.id,
            "name": self.path,
            "path": self.path,
        }


class File:
    """Class representing a file"""

    id: str
    path: str
    name: str
    dir: str
    source: bool
    error: str
    # dir_ptr: Dir

    def __init__(self, path: str):
        self.id = caculate_hash_id(path)
        self.path = path
        self.name = os.path.basename(path)
        dir = os.path.dirname(path)
        if dir == "":
            self.dir = "."
        else:
            self.dir = dir
        self.source = False
        self.error = ""
        # self.dir_ptr

    def dump(self) -> SourceFile:
        result = {
            "id": self.id,
            "name": self.name,
            "path": self.dir,
            "pkg": "",
            "deps": [],
        }
        return result


class Dep:
    """Class representing a dependency"""

    id: str
    name: str
    typ: str
    file_ptr: str

    def __init__(self, file: File):
        self.id = caculate_hash_id(file.name)
        self.name = file.name
        self.typ = "file"
        self.file_ptr = file

    def dump(self) -> SourceDep:
        result = {
            "id": self.id,
            "name": self.name,
            "type": self.typ,
            "ref": "",
        }
        return result
