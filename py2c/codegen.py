from py2c.ir import *


class CCodeGenerator:
    def __init__(self):
        self.lines = []
        self.indent = 0
        self.declared = set()

    def generate(self, ir):
        self._emit("#include <stdio.h>")
        self._emit("")

        # Emit functions first
        for stmt in ir.statements:
            if isinstance(stmt, IRFunction):
                self._gen_function(stmt)
                self._emit("")

        # Emit main
        self._emit("int main() {")
        self.indent += 1

        for stmt in ir.statements:
            if not isinstance(stmt, IRFunction):
                self._gen(stmt)

        self._emit("return 0;")
        self.indent -= 1
        self._emit("}")

        return "\n".join(self.lines)

    def _emit(self, line):
        self.lines.append("    " * self.indent + line)

    # ---------- FUNCTION ----------

    def _gen_function(self, node):
        params = ", ".join(f"int {p.name}" for p in node.params)
        self._emit(f"int {node.name}({params}) {{")
        self.indent += 1
        for stmt in node.body:
            self._gen(stmt)
        self.indent -= 1
        self._emit("}")

    # ---------- STATEMENTS ----------

    def _gen(self, node):
        if isinstance(node, IRProgram):
            for s in node.statements:
                self._gen(s)

        elif isinstance(node, IRAssign):
            name = node.target.name
            expr = self._expr(node.value)
            if name not in self.declared:
                self.declared.add(name)
                self._emit(f"int {name} = {expr};")
            else:
                self._emit(f"{name} = {expr};")

        elif isinstance(node, IRCall):
            self._emit(f"{self._expr(node)};")

        elif isinstance(node, IRFor):
            var = node.var.name
            if var not in self.declared:
                self.declared.add(var)
                init = f"int {var} = {self._expr(node.start)}"
            else:
                init = f"{var} = {self._expr(node.start)}"

            self._emit(f"for ({init}; {var} < {self._expr(node.end)}; {var} += {self._expr(node.step)}) {{")
            self.indent += 1
            for s in node.body:
                self._gen(s)
            self.indent -= 1
            self._emit("}")

        elif isinstance(node, IRWhile):
            self._emit(f"while {self._expr(node.condition)} {{")
            self.indent += 1
            for s in node.body:
                self._gen(s)
            self.indent -= 1
            self._emit("}")

        elif isinstance(node, IRIf):
            self._emit(f"if {self._expr(node.condition)} {{")
            self.indent += 1
            for s in node.then_body:
                self._gen(s)
            self.indent -= 1
            self._emit("}")

            if node.else_body:
                self._emit("else {")
                self.indent += 1
                for s in node.else_body:
                    self._gen(s)
                self.indent -= 1
                self._emit("}")

        elif isinstance(node, IRReturn):
            self._emit(f"return {self._expr(node.value)};")

        elif isinstance(node, IRPrint):
            fmt = " ".join("%d" for _ in node.values) + "\\n"
            args = ", ".join(self._expr(v) for v in node.values)
            self._emit(f'printf("{fmt}", {args});')

        elif isinstance(node, IRBreak):
            self._emit("break;")

        elif isinstance(node, IRContinue):
            self._emit("continue;")

        elif isinstance(node, IRPass):
            pass

    # ---------- EXPRESSIONS ----------

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
            return f"!{self._expr(node.value)}"
        if isinstance(node, IRCall):
            return f"{node.name}({', '.join(self._expr(a) for a in node.args)})"

        raise NotImplementedError(f"Expression not supported: {type(node)}")

    def _map_op(self, op):
        return {
            "Add": "+",
            "Sub": "-",
            "Mult": "*",
            "Div": "/",
            "Mod": "%"
        }[op]
