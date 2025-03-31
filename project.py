from sourcecode import Dir, File, Dep
import os
from common import DepType
from monty import PARSER_NAME, VESION, LANG, TYPE_NORMAL

from protocol.map import Source
from datetime import datetime, timezone

class Project:
    """Class representing a project"""

    name: str
    path: str
    excludes: set
    directory: str
    dirs: dict[str, Dir]
    files: dict[str, File]
    deps: dict[str, Dep]

    def __init__(self, name: str, path: str, directory: str, excludes: str):
        self.name = name
        self.path = path
        self.directory = directory
        self.dirs = {}
        self.files = {}
        self.deps = {}
        self.excludes = set()
        if excludes != "":
            excludes_list = excludes.split(",")
            for excl in excludes_list:
                excl_normalized = os.path.join(path, excl.strip())
                excl_absp = os.path.abspath(excl_normalized)
                self.excludes.add(excl_absp)

    def scan(self):
        os.chdir(self.path)
        if os.path.isdir(self.directory):
            root = Dir(self.directory)
            self.dirs[self.directory] = root
            self.deps[self.directory] = Dep(root, DepType.PKG)
            self.deps[""] = Dep(root, DepType.PKG)
            self.traverse(self.directory)

    def traverse(self, dir: str):
        entries = os.listdir(dir)
        for entry in entries:
            current_entry = os.path.join(dir, entry)
            absp = os.path.abspath(current_entry)
            if absp in self.excludes:
                continue
            if current_entry.startswith("./"):
                current_entry = current_entry[2:]
            isDir = os.path.isdir(current_entry)
            if isDir:
                pkg = Dir(current_entry)
                self.dirs[current_entry] =pkg
                self.deps[current_entry] = Dep(pkg, DepType.PKG)
                self.traverse(current_entry)
            else:
                d = self.lookup(dir, 1)

                assert d != None and d.typ == DepType.PKG

                file = File(current_entry, d.pkg_ptr)
                self.deps[current_entry] = Dep(file, DepType.FILE)
                self.files[current_entry] = file

    def parse_files(self):
        for f in self.files.values():
            if f.source:
                f.parse(self.lookup)

    def build_dependencies(self):
        for f in self.files.values():
            if f.source:
                f.connect()

        for f in self.files.values():
            if f.source:
                f.liftup()
    
    def complete_fields(self):
        pass
    
    # 0: all, 1: pkg, 2: file
    def lookup(self, name: str, typ: int) -> Dep|None:
        if typ == 2:
            return self.deps.get(name+".py")
        if typ == 1:
            return self.deps.get(name)
        else:
            r = self.deps.get(name)
            if r != None:
                return r
            return self.deps.get(name+".py")

    def dump(self) -> Source:
        now = datetime.now(timezone.utc).astimezone()

        result = {
            "name": self.name,
            "lang": LANG,
            "parser": "%s %s"%(PARSER_NAME, VESION),
            "typ": TYPE_NORMAL,
            "timestamp": now.isoformat(),
            "repository": "",
            "version": "",
            "pkgs": [],
            "files": [],
            "absts": [],
            "fns": [],
            "calls": [],
            "deps": [],
            "refs": [],
        }
        for p in self.dirs.values():
            result["pkgs"].append(p.dump())
        for f in self.files.values():
            result["files"].append(f.dump())
        for d in self.deps.values():
            if d.typ == DepType.PKG:
                continue
            result["deps"].append(d.dump())
        return result
