from py2c.ir import *

class CCodeGenerator:
    def __init__(self):
        self.lines = []
        self.indent = 0
        self.declared = set()

    # ---------- PUBLIC API ----------
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

    # ---------- HELPERS ----------
    def _emit(self, line):
        self.lines.append("    " * self.indent + line)

    # ---------- STATEMENTS ----------
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
            loop_var = node.var.name
            if loop_var not in self.declared:
                self.declared.add(loop_var)
                init = f"int {loop_var} = {self._expr(node.start)}"
            else:
                init = f"{loop_var} = {self._expr(node.start)}"
            end = self._expr(node.end)
            step = self._expr(getattr(node, "step", IRConst(1)))  # default step=1
            self._emit(f"for ({init}; {loop_var} < {end}; {loop_var}+={step}) {{")
            self.indent += 1
            for stmt in node.body:
                self._gen(stmt)
            self.indent -= 1
            self._emit("}")

        elif isinstance(node, IRIf):
            self._gen_if(node)

        else:
            raise NotImplementedError(f"Codegen not implemented for {type(node)}")

    # ---------- IF / ELIF / ELSE ----------
    def _gen_if(self, node):
        cond = self._expr(node.condition)
        self._emit(f"if ({cond}) {{")
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

    # ---------- EXPRESSIONS ----------
    def _expr(self, node):
        if isinstance(node, IRConst):
            return str(node.value)
        if isinstance(node, IRVar):
            return node.name
        if isinstance(node, IRBinOp):
            if node.op not in ("Add", "Sub", "Mult", "Div", "Mod"):
                raise NotImplementedError(f"Unsupported binary op: {node.op}")
            left = self._expr(node.left)
            right = self._expr(node.right)
            return f"({left} {self._map_op(node.op)} {right})"
        if isinstance(node, IRCompare):
            left = self._expr(node.left)
            right = self._expr(node.right)
            return f"({left} {node.op} {right})"
        if isinstance(node, IRBoolOp):
            op = "&&" if node.op == "and" else "||"
            parts = [self._expr(v) for v in node.values]
            return "(" + f" {op} ".join(parts) + ")"
        if isinstance(node, IRNot):
            return f"(!{self._expr(node.value)})"
        raise NotImplementedError(f"Expression not supported: {type(node)}")

    # ---------- OPERATOR MAP ----------
    def _map_op(self, op):
        return {
            "Add": "+",
            "Sub": "-",
            "Mult": "*",
            "Div": "/",
            "Mod": "%"
        }[op]
