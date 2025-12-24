import ast

class Py2CParser:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tree = ast.parse(source_code)

    def dump_ast(self):
        return ast.dump(self.tree, indent=2)
