import ast
import os

from nodes import Abstract, Call, Callabale


class Parser:
    name: str
    path: str
    deps: dict[str, any]
    fns: dict[str, Callabale]
    absts: dict[str, Abstract]
    cs: list[Call]
    ast: any
    file: any
    lookup: any
    visited_set: set

    """Class representing a parser"""

    def __init__(self, file: any, lookup: any):
        self.name = file.name
        self.path = file.dir.path
        self.ast = file.ast
        self.file = file
        self.deps = {}
        self.fns = {}
        self.absts = {}
        self.cs = []
        self.visited_set = set()
        self.lookup = lookup

    def parse_source(self):
        for node in ast.walk(self.ast):
            self.parse_node(node)

        self.post_walk()

    def post_walk(self):
        for fn in self.fns.values():
            if fn.method:
                fn.abstract = self.absts.get(fn.abstract).id
            else:
                fn.abstract = ""

    def parse_node(self, node):
        if isinstance(node, ast.Import):
            self.parse_import(node)
        elif isinstance(node, ast.ImportFrom):
            self.parse_import_from(node)
        elif isinstance(node, ast.FunctionDef):
            self.parse_function_def(node)
        elif isinstance(node, ast.ClassDef):
            self.parse_class_def(node)
        elif isinstance(node, ast.Call):
            self.parse_call(node)

    def parse_import(self, node):
        for alias in node.names:
            key = alias.asname if alias.asname is not None else alias.name
            lookup_name = os.path.join(self.path, alias.name.replace(".", "/"))
            r = self.lookup(lookup_name + "__init__", 2)
            if r is not None:
                self.deps[key] = r
            else:
                r = self.lookup(lookup_name, 2)
                if r is not None:
                    self.deps[key] = r

    def try_import_pkg(self, key: str, pkg: str, names: any):
        match = False
        # match files
        for alias in names:
            key = alias.asname if alias.asname is not None else alias.name
            lookup_name = os.path.join(pkg, alias.name)
            r = self.lookup(lookup_name, 2)
            if r is not None:
                self.deps[key] = r
                match = True

        if not match:
            lookup_name = os.path.join(pkg, "__init__")
            r = self.lookup(lookup_name, 2)
            if r is not None:
                self.deps[key] = r
            # match file
            else:
                r = self.lookup(pkg, 2)
                if r is not None:
                    self.deps[key] = r

    def parse_import_from(self, node):
        if node.level > 0:
            relative_path = "../" * (node.level - 1) + (
                node.module.replace(".", "/") if node.module else ""
            )
            key = ""
            if node.module:
                keys: list = node.module.split(".")
                key = keys[len(keys) - 1]
            lookup_name = os.path.normpath(os.path.join(self.path, relative_path))
            # lookup the package
            # perhaps: from package import file, from package import function(__init__), from package.package import xx
            r = self.lookup(lookup_name, 0)
            if r is not None:
                self.try_import_pkg(key, lookup_name, node.names)

        else:
            # lookup_name = os.path.normpath(os.path.join(self.path, node.module.replace('.', '/')))
            lookup_name = os.path.normpath(node.module.replace(".", "/"))
            keys: list = node.module.split(".")
            key = keys[len(keys) - 1]
            r = self.lookup(lookup_name, 0)
            if r is not None:
                self.try_import_pkg(key, lookup_name, node.names)

    def parse_function_def(self, node):
        if node in self.visited_set:
            return
        fn = Callabale("", node, self.file)
        self.fns[node.name] = fn

    def parse_class_def(self, node):
        fields = []
        for body_item in node.body:
            if isinstance(body_item, ast.Assign):
                for target in body_item.targets:
                    if isinstance(target, ast.Name):
                        fields.append(target.id)

            elif isinstance(body_item, ast.FunctionDef):
                fn = Callabale(node.name, body_item, self.file)
                self.fns["%s.%s" % (node.name, body_item.name)] = fn
                self.visited_set.add(body_item)

            self.absts[node.name] = Abstract(node, fields, self.file)

    def parse_call(self, node):
        if not isinstance(node.func, ast.Name):
            return
        # arg_values = [ast.dump(arg) for arg in node.args]
        # callee = node.func.id
        # self.cs.append(Call("callerA", callee, "typ", node, self.file))
        # TODO: impl call, save decl in stack to pop up the caller
        pass
