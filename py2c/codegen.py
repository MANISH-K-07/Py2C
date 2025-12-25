from py2c.ir import *


class CCodeGenerator:
    def __init__(self):
        self.lines = []
        self.indent = 0
        self.declared = set()

    def generate(self, ir):
        self._emit("#include <stdio.h>")
        self._emit("")
        self._emit("int main() {")
        self.indent += 1
        self._gen(ir)
        self._emit("return 0;")
        self.indent -= 1
        self._emit("}")
        return "\n".join(self.lines)

    def _emit(self, line):
        self.lines.append("    " * self.indent + line)

    def _gen(self, node):
        if isinstance(node, IRProgram):
            for stmt in node.statements:
                self._gen(stmt)

        elif isinstance(node, IRAssign):
            name = node.target.name
            expr = self._expr(node.value)
            if name not in self.declared:
                self.declared.add(name)
                self._emit(f"int {name} = {expr};")
            else:
                self._emit(f"{name} = {expr};")

        elif isinstance(node, IRFor):
            var = node.var.name
            if var not in self.declared:
                self.declared.add(var)
                init = f"int {var} = {self._expr(node.start)}"
            else:
                init = f"{var} = {self._expr(node.start)}"

            end = self._expr(node.end)
            step = self._expr(node.step)

            self._emit(f"for ({init}; {var} < {end}; {var} += {step}) {{")
            self.indent += 1
            for stmt in node.body:
                self._gen(stmt)
            self.indent -= 1
            self._emit("}")

        elif isinstance(node, IRWhile):
            cond = self._expr(node.condition)
            self._emit(f"while {cond} {{")
            self.indent += 1
            for stmt in node.body:
                self._gen(stmt)
            self.indent -= 1
            self._emit("}")

        elif isinstance(node, IRIf):
            self._gen_if(node)

        elif isinstance(node, IRBreak):
            self._emit("break;")

        elif isinstance(node, IRContinue):
            self._emit("continue;")

        else:
            raise NotImplementedError(f"Codegen not implemented for {type(node)}")

    def _gen_if(self, node):
        cond = self._expr(node.condition)
        self._emit(f"if {cond} {{")
        self.indent += 1
        for stmt in node.then_body:
            self._gen(stmt)
        self.indent -= 1
        self._emit("}")

        if node.else_body:
            if len(node.else_body) == 1 and isinstance(node.else_body[0], IRIf):
                self._emit("else ")
                self._gen_if(node.else_body[0])
            else:
                self._emit("else {")
                self.indent += 1
                for stmt in node.else_body:
                    self._gen(stmt)
                self.indent -= 1
                self._emit("}")

    def _expr(self, node):
        if isinstance(node, IRConst):
            return str(node.value)

        if isinstance(node, IRVar):
            return node.name

        if isinstance(node, IRBinOp):
            return f"({self._expr(node.left)} {self._map_op(node.op)} {self._expr(node.right)})"

        if isinstance(node, IRCompare):
            return f"({self._expr(node.left)} {node.op} {self._expr(node.right)})"

        if isinstance(node, IRBoolOp):
            op = "&&" if node.op == "and" else "||"
            return "(" + f" {op} ".join(self._expr(v) for v in node.values) + ")"

        if isinstance(node, IRNot):
            return f"(!{self._expr(node.value)})"

        raise NotImplementedError(f"Expression not supported: {type(node)}")

    def _map_op(self, op):
        return {
            "Add": "+",
            "Sub": "-",
            "Mult": "*",
            "Div": "/",
            "Mod": "%"
        }[op]
