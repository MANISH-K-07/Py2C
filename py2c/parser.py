import ast
from py2c.ir import (
    IRProgram,
    IRAssign,
    IRVar,
    IRConst,
    IRBinOp,
    IRFor,
)


class Py2CParser:
    def __init__(self, source_code: str):
        self.tree = ast.parse(source_code)

    def parse(self):
        statements = []
        for stmt in self.tree.body:
            statements.append(self._parse_stmt(stmt))
        return IRProgram(statements)

    def _parse_stmt(self, stmt):
        if isinstance(stmt, ast.Assign):
            target = stmt.targets[0].id
            value = self._parse_expr(stmt.value)
            return IRAssign(IRVar(target), value)

        if isinstance(stmt, ast.For):
            var = IRVar(stmt.target.id)

            if not isinstance(stmt.iter, ast.Call) or stmt.iter.func.id != "range":
                raise NotImplementedError("Only range() loops supported")

            start = self._parse_expr(stmt.iter.args[0])
            end = self._parse_expr(stmt.iter.args[1])

            body = [self._parse_stmt(s) for s in stmt.body]
            return IRFor(var, start, end, body)

        raise NotImplementedError(f"Unsupported statement: {type(stmt)}")

    def _parse_expr(self, expr):
        if isinstance(expr, ast.Constant):
            return IRConst(expr.value)

        if isinstance(expr, ast.Name):
            return IRVar(expr.id)

        if isinstance(expr, ast.BinOp):
            left = self._parse_expr(expr.left)
            right = self._parse_expr(expr.right)
            op = type(expr.op).__name__
            return IRBinOp(left, op, right)

        raise NotImplementedError(f"Unsupported expression: {type(expr)}")
