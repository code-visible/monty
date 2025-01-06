from utils import caculate_hash_id  # type: ignore
import os


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

    def dump(self):
        return {}


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
        # self.dir_ptr
        self.id = caculate_hash_id(path)
        self.path = path
        self.name = os.path.basename(path)
        self.dir = os.path.dirname(path)
        self.source = False
        self.error = ""
        # self.dir_ptr

    def dump(self):
        return {}


class Dep:
    """Class representing a dependency"""

    id: str
    name: str
    typ: str
    file_ptr: str

    def __init__(self, file: File):
        self.id = ""
        self.name = file.name
        self.typ = "file"
        self.file_ptr = file

    def dump(self):
        return {}
