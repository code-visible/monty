from utils import caculate_hash_id  # type: ignore
from protocol.callable import SourceCallable
from protocol.abstract import SourceAbstract

class Callabale:
    """Class representing a Python function"""

    pos: str
    name: str
    signature: str
    abstract: str
    file: any # File
    comment: str
    parameters: list[str]
    method: bool
    node: any

    def __init__(self, abst: str, node: any, file: any):
        param_names = [arg.arg for arg in node.args.args]
        pos = "%s:%s:%s"%(file.path, node.lineno, node.col_offset)
        self.pos = pos
        self.id = caculate_hash_id(pos)
        self.node = node
        self.name = node.name
        self.signature = "%s(%s)"%(node.name, ", ".join(param_names))
        self.abstract = abst
        self.file = file
        self.comment = ""
        self.parameters = param_names
        self.method = False if abst == "" else True

    def dump(self) -> SourceCallable:
        return {
            "id": self.id,
            "pos": self.pos,
            "name": self.name,
            "signature": self.signature,
            "abstract": self.abstract,
            "file": self.file.id,
            "comment": self.comment,
            "parameters": self.parameters,
            "results": [],
            "method": self.method,
            "private": False,
        }

class Abstract:
    """Class representing a Python class"""

    pos: str
    name: str
    file: any # File
    comment: str
    fields: list[str]
    node: any

    def __init__(self, node: any, fields: list[str], file: any):
        pos = "%s:%s:%s"%(file.path, node.lineno, node.col_offset)
        self.pos = pos
        self.id = caculate_hash_id(pos)
        self.node = node
        self.name = node.name
        self.file = file
        self.comment = ""
        self.fields = fields

    def dump(self) -> SourceAbstract:
        return {
            "id": self.id,
            "pos": self.pos,
            "name": self.name,
            "file": self.file.id,
            "comment": self.comment,
            "fields": self.fields,
        }

class Call:
    """Class representing a Python class"""

    pos: str
    caller: str
    callee: str
    file: any # File
    type: str

    def __init__(self, caller: str, callee: str, typ: str, node: any, file: any):
        pos = "%s:%s:%s"%(file.path, node.lineno, node.col_offset)
        self.pos = pos
        self.id = caculate_hash_id(pos)
        self.caller = caller
        self.file =file
        self.callee = callee
        self.type = typ

    def dump(self) -> SourceAbstract:
        return {
            "id": self.id,
            "pos": self.pos,
            "name": self.name,
            "file": self.file.id,
            "comment": self.comment,
            "fields": self.fields,
        }