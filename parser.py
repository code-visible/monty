import ast


class Parser:
    name: str
    path: str
    deps: dict[str, any]
    ast: any
    lookup: any

    """Class representing a parser"""

    def __init__(self, name, path: str, ast: any, lookup: any):
        self.name = name
        self.path = path
        self.ast = ast
        self.deps = {}
        self.lookup = lookup

    def parse_source(self):
        for node in ast.walk(self.ast):
            self.parse_node(node)

    # TODO: impl parse
    def parse_node(self, node):
        pass