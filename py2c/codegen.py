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
            name, expr = node.target.name, self._expr(node.value)
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
            self._emit(f"for ({init}; {var} < {self._expr(node.end)}; {var} += {self._expr(node.step)}) {{")
            self.indent += 1
            for stmt in node.body:
                self._gen(stmt)
            self.indent -= 1
            self._emit("}")

        elif isinstance(node, IRWhile):
            self._emit(f"while ({self._expr(node.condition)}) {{")
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

        elif isinstance(node, IRPass):
            pass

        elif isinstance(node, IRPrint):
            fmt = " ".join("%d" for _ in node.values) + "\\n"
            args = ", ".join(self._expr(v) for v in node.values)
            self._emit(f'printf("{fmt}", {args});' if args else f'printf("\\n");')

        # ---------- Functions / Return ----------
        elif isinstance(node, IRFunction):
            params_str = ", ".join(f"int {p.name}" for p in node.params)
            self._emit(f"int {node.name}({params_str}) {{")
            self.indent += 1
            for stmt in node.body:
                self._gen(stmt)
            self.indent -= 1
            self._emit("}")

        elif isinstance(node, IRReturn):
            self._emit(f"return {self._expr(node.value)};")

        elif isinstance(node, IRCall):
            args_str = ", ".join(self._expr(arg) for arg in node.args)
            return f"{node.name}({args_str})"

        else:
            raise NotImplementedError(f"Codegen not implemented for {type(node)}")

    def _gen_if(self, node):
        self._emit(f"if ({self._expr(node.condition)}) {{")
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
        if isinstance(node, IRConst): return str(node.value)
        if isinstance(node, IRVar): return node.name
        if isinstance(node, IRBinOp): return f"({self._expr(node.left)} {self._map_op(node.op)} {self._expr(node.right)})"
        if isinstance(node, IRCompare): return f"({self._expr(node.left)} {node.op} {self._expr(node.right)})"
        if isinstance(node, IRBoolOp): return "(" + f" {('&&' if node.op=='and' else '||')} ".join(self._expr(v) for v in node.values) + ")"
        if isinstance(node, IRNot): return f"(!{self._expr(node.value)})"
        if isinstance(node, IRCall):
            args_str = ", ".join(self._expr(arg) for arg in node.args)
            return f"{node.name}({args_str})"
        raise NotImplementedError(f"Expression not supported: {type(node)}")

    def _map_op(self, op):
        return {"Add": "+", "Sub": "-", "Mult": "*", "Div": "/", "Mod": "%"}[op]
