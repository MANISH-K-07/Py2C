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


class IRCompare(IRNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"IRCompare({self.left} {self.op} {self.right})"


class IRBoolOp(IRNode):
    def __init__(self, op, values):
        self.op = op
        self.values = values

    def __repr__(self):
        return f"IRBoolOp({self.op}, {self.values})"


class IRNot(IRNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"IRNot({self.value})"


class IRFor(IRNode):
    def __init__(self, var, start, end, step, body):
        self.var = var
        self.start = start
        self.end = end
        self.step = step
        self.body = body

    def __repr__(self):
        return f"IRFor({self.var}, {self.start}, {self.end}, {self.step}, {self.body})"


class IRWhile(IRNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"IRWhile({self.condition}, {self.body})"


class IRIf(IRNode):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body or []

    def __repr__(self):
        return f"IRIf({self.condition}, then={self.then_body}, else={self.else_body})"


class IRBreak(IRNode):
    def __repr__(self):
        return "IRBreak()"


class IRContinue(IRNode):
    def __repr__(self):
        return "IRContinue()"


class IRPrint(IRNode):
    def __init__(self, values):
        self.values = values


class IRPass(IRNode):
    def __repr__(self):
        return "IRPass()"


# ---------- Functions ----------
class IRFunction(IRNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params  # list of IRVar
        self.body = body      # list of IR statements

    def __repr__(self):
        return f"IRFunction({self.name}, params={self.params}, body={self.body})"


class IRReturn(IRNode):
    def __init__(self, value):
        self.value = value  # IR expression

    def __repr__(self):
        return f"IRReturn({self.value})"


class IRCall(IRNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args  # list of IR expressions

    def __repr__(self):
        return f"IRCall({self.name}, {self.args})"
