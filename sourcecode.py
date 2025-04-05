import ast
import os
from parser import Parser
from typing import Self

from common import DepType
from protocol.dep import SourceDep
from protocol.file import SourceFile
from protocol.pkg import SourcePkg
from utils import (
    caculate_hash_id,  # type: ignore
    format_path,
    is_source,
)


class Dir:
    """Class representing a directory"""

    id: str
    path: str
    files: int
    pkg: bool
    imps: set[Self]

    def __init__(self, path: str):
        self.id = caculate_hash_id(path)
        self.path = path
        self.files = 0
        self.pkg = False
        self.imps = set()

    def dump(self) -> SourcePkg:
        noramlized_path = format_path(self.path)
        imports = []
        for i in self.imps:
            imports.append(i.id)
        name = os.path.basename(noramlized_path)
        return {
            "id": self.id,
            "name": "/" if name == "" else name,
            "path": noramlized_path,
            "imports": imports,
            "deps": [],
        }


class File:
    """Class representing a file"""

    id: str
    path: str
    name: str
    dir: Dir
    source: bool
    ast: any
    error: str
    parser: Parser | None
    imps: set[Self]

    def __init__(self, path: str, dir: Dir):
        assert dir is not None

        self.id = caculate_hash_id(path)
        self.path = path
        self.name = os.path.basename(path)
        self.dir = dir
        self.source = is_source(path)
        self.error = ""
        self.ast = None
        self.parser = None
        self.dir_ptr = None
        self.imps = set()

    def parse(self, lookup: any):
        with open(self.path, "r") as file:
            content = file.read()
            self.ast = ast.parse(content)
        self.parser = Parser(self, lookup)
        self.parser.parse_source()

    def connect(self):
        for d in self.parser.deps.values():
            if d.typ == DepType.FILE:
                f = d.file_ptr
                self.imps.add(f)

    def liftup(self):
        for f in self.imps:
            if self.dir != f.dir:
                self.dir.imps.add(f.dir)

    def dump(self) -> SourceFile:
        noramlized_path = format_path(self.dir.path)
        imports = []
        if self.source:
            for i in self.imps:
                imports.append(i.id)
        # TODO: support normal deps in import parse
        # deps = set()
        # if self.source:
        #     for d in self.parser.deps.values():
        #         deps.add(d.id)
        result = {
            "id": self.id,
            "name": self.name,
            "path": noramlized_path,
            "source": self.source,
            "parsed": self.ast is not None,
            "error": "",
            "pkg": self.dir.id,
            "imports": imports,
            # "deps": [item for item in deps],
            "deps": [],
        }
        return result


class Dep:
    """Class representing a dependency"""

    id: str
    name: str
    typ: DepType
    file_ptr: str
    pkg_ptr: str

    def __init__(self, ptr: File | Dir, typ: DepType):
        self.id = caculate_hash_id(ptr.path)
        self.name = ptr.path
        self.typ = typ
        if typ == DepType.PKG:
            self.pkg_ptr = ptr
        else:
            self.file_ptr = ptr

    def dump(self) -> SourceDep:
        assert self.typ != DepType.PKG
        type = "file"
        if self.typ == DepType.MOD:
            type = "mod"
        else:
            # trapped into panic
            type = "pkg"
        result = {
            "id": self.id,
            "name": self.name,
            "type": type,
            "ref": "",
        }
        return result
