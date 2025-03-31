from sourcecode import Dir, File, Dep
import os
from common import DepType
from monty import PARSER_NAME, VESION, LANG, TYPE_NORMAL, DEFAULT_EXCLUDE_DIRECTORIES, DEFAULT_INCLUDE_FILE_TYPES

from protocol.map import Source
from datetime import datetime, timezone

class Project:
    """Class representing a project"""

    name: str
    path: str
    abs_path: str
    excludes: set
    excludes_dot: bool
    includes: set
    includes_file_types: set
    directory: str
    dirs: dict[str, Dir]
    files: dict[str, File]
    deps: dict[str, Dep]

    def __init__(self, name: str, path: str, directory: str, excludes: str, file_types: str):
        self.name = name
        self.path = path
        self.abs_path = os.path.abspath(path)
        self.directory = directory
        self.dirs = {}
        self.files = {}
        self.deps = {}
        self.excludes = set()
        self.excludes_dot = False
        self.includes = set()
        self.includes_file_types = set()
        self.includes_file_types.add("py")

        self.build_excludes(excludes)
        self.parse_file_types(file_types)
    
    def build_excludes(self, excls: str):
        excludes_list = excls.split(",")
        for excl in excludes_list:
            excl_normalized = excl.strip()
            if excl_normalized == ".*":
                self.excludes_dot = True
            else:
                excl_absp = os.path.join(self.abs_path, excl_normalized)
                self.excludes.add(excl_absp)
    
    def parse_file_types(self, file_types: str):
        file_types_list = file_types.split(",")
        for typ in file_types_list:
            if typ.startswith("*."):
                self.includes_file_types.add(typ[2:])
            else:
                self.includes.add(typ)

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
            if self.excludes_dot and entry.startswith("."):
                continue
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
                should_parse = False
                if entry in self.includes:
                    should_parse = True
                if not should_parse:
                    file_segements = entry.split(".")
                    if len(file_segements) > 1:
                        if file_segements[-1] in self.includes_file_types:
                            should_parse = True
                if not should_parse:
                    continue
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
        for f in self.files.values():
            if f.source:
                for fn in f.parser.fns.values():
                    result["fns"].append(fn.dump())
                for abst in f.parser.absts.values():
                    result["absts"].append(abst.dump())
        return result
