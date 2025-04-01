import ast
from nodes import Callabale, Abstract, Call

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
            pass

    def parse_import(self, node):
        pass

    def parse_import_from(self, node):
        pass

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
                self.fns["%s.%s"%(node.name, body_item.name)] = fn
                self.visited_set.add(body_item)

            self.absts[node.name] = Abstract(node, fields, self.file)

