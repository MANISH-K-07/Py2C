from py2c.ir import (
    IRProgram,
    IRAssign,
    IRConst,
    IRVar,
    IRBinOp,
    IRFor,
    IRIf,
    IRCompare,
)


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

    # ---------- helpers ----------

    def _emit(self, line):
        self.lines.append("    " * self.indent + line)

    def _gen_condition(self, cond):
        left = self._expr(cond.left)
        right = self._expr(cond.right)
        return f"{left} {cond.op} {right}"

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

            self._emit(f"for ({init}; {loop_var} < {end}; {loop_var}++) {{")
            self.indent += 1

            for stmt in node.body:
                self._gen(stmt)

            self.indent -= 1
            self._emit("}")

        elif isinstance(node, IRIf):
            cond = self._gen_condition(node.condition)
            self._emit(f"if ({cond}) {{")
            self.indent += 1

            for stmt in node.then_body:
                self._gen(stmt)

            self.indent -= 1
            self._emit("}")

            if node.else_body:
                self._emit("else {")
                self.indent += 1

                for stmt in node.else_body:
                    self._gen(stmt)

                self.indent -= 1
                self._emit("}")

        else:
            raise NotImplementedError(f"Codegen not implemented for {type(node)}")

    def _expr(self, node):
        if isinstance(node, IRConst):
            return str(node.value)

        if isinstance(node, IRVar):
            return node.name

        if isinstance(node, IRBinOp):
            left = self._expr(node.left)
            right = self._expr(node.right)
            op = self._map_op(node.op)
            return f"({left} {op} {right})"

        if isinstance(node, IRCompare):
            left = self._expr(node.left)
            right = self._expr(node.right)
            return f"{left} {node.op} {right}"

        raise NotImplementedError(f"Expression not supported: {type(node)}")

    def _map_op(self, op):
        return {
            "Add": "+",
            "Sub": "-",
            "Mult": "*",
            "Div": "/",
        }[op]
