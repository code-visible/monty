from sourcecode import Dir, File, Dep
import os

from protocol.map import Source


class Project:
    """Class representing a project"""

    name: str
    path: str
    directory: str
    dirs: dict[str, Dir]
    files: dict[str, File]
    deps: dict[str, Dep]

    def __init__(self, name: str, path: str, directory: str):
        self.name = name
        self.path = path
        self.directory = directory
        self.dirs = {}
        self.files = {}
        self.deps = {}

    def scan(self):
        os.chdir(self.path)
        if os.path.isdir(self.directory):
            self.dirs[self.directory] = Dir(self.directory)
            self.traverse(self.directory)

    def traverse(self, dir: str):
        entries = os.listdir(dir)
        for entry in entries:
            current_entry = os.path.join(dir, entry)
            if current_entry.startswith("./"):
                current_entry = current_entry[2:]
            isDir = os.path.isdir(current_entry)
            if isDir:
                self.dirs[current_entry] = Dir(current_entry)
                self.traverse(current_entry)
            else:
                file = File(current_entry)
                self.files[current_entry] = file
                self.deps[current_entry] = Dep(file)

    def parse_files(self):
        pass

    def dump(self) -> Source:
        result = {
            "name": self.name,
            "directory": self.directory,
            "language": "python",
            "pkgs": [],
            "files": [],
            "abstracts": [],
            "callables": [],
            "calls": [],
            "deps": [],
        }
        for p in self.dirs.values():
            result["pkgs"].append(p.dump())
        for f in self.files.values():
            result["files"].append(f.dump())
        for d in self.deps.values():
            result["deps"].append(d.dump())
        return result
