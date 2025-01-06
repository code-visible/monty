from sourcecode import Dir, File, Dep
import os


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
            isDir = os.path.isdir(entry)
            if isDir:
                self.dirs[entry] = Dir(entry)
                self.traverse(entry)
            else:
                file = File(entry)
                self.files[entry] = file
                self.deps[entry] = Dep(file)

    def parse_files(self):
        pass

    def dump(self):
        return {}
