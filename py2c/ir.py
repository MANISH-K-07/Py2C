class IRNode:
    pass


class IRProgram(IRNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"IRProgram({self.statements})"


class IRAssign(IRNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value

    def __repr__(self):
        return f"IRAssign({self.target}, {self.value})"


class IRVar(IRNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IRVar({self.name})"


class IRConst(IRNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"IRConst({self.value})"


class IRBinOp(IRNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"IRBinOp({self.left} {self.op} {self.right})"


class IRCompare:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # string: < > <= >= ==
        self.right = right

    def __repr__(self):
        return f"IRCompare({self.left} {self.op} {self.right})"


class IRFor(IRNode):
    def __init__(self, var, start, end, body):
        self.var = var
        self.start = start
        self.end = end
        self.body = body

    def __repr__(self):
        return f"IRFor({self.var}, {self.start}, {self.end}, {self.body})"


class IRIf:
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body or []

    def __repr__(self):
        return f"IRIf({self.condition}, then={self.then_body}, else={self.else_body})"
