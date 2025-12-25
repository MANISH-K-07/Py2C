import ast
from py2c.ir import (
    IRProgram,
    IRAssign,
    IRVar,
    IRConst,
    IRBinOp,
    IRFor,
    IRIf,
    IRCompare,
)


class Py2CParser:
    def __init__(self, source_code: str):
        self.tree = ast.parse(source_code)

    def parse(self):
        statements = []
        for stmt in self.tree.body:
            statements.append(self._parse_stmt(stmt))
        return IRProgram(statements)

    # ---------- STATEMENTS ----------

    def _parse_stmt(self, stmt):
        if isinstance(stmt, ast.Assign):
            target = stmt.targets[0].id
            value = self._parse_expr(stmt.value)
            return IRAssign(IRVar(target), value)

        elif isinstance(stmt, ast.For):
            var = IRVar(stmt.target.id)

            if not isinstance(stmt.iter, ast.Call) or stmt.iter.func.id != "range":
                raise NotImplementedError("Only range() loops supported")

            start = self._parse_expr(stmt.iter.args[0])
            end = self._parse_expr(stmt.iter.args[1])

            body = [self._parse_stmt(s) for s in stmt.body]
            return IRFor(var, start, end, body)

        elif isinstance(stmt, ast.If):
            return self.parse_if(stmt)

        raise NotImplementedError(f"Unsupported statement: {type(stmt)}")

    # ---------- EXPRESSIONS ----------

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

        if isinstance(expr, ast.UnaryOp):
            # Handle negative numbers: -x → (0 - x)
            if isinstance(expr.op, ast.USub):
                operand = self._parse_expr(expr.operand)
                return IRBinOp(IRConst(0), "Sub", operand)

            if isinstance(expr.op, ast.UAdd):
                return self._parse_expr(expr.operand)

            raise NotImplementedError("Unsupported unary operator")

        raise NotImplementedError(f"Unsupported expression: {type(expr)}")

    # ---------- IF / ELIF / ELSE ----------

    def parse_if(self, stmt):
        condition = self.parse_compare(stmt.test)

        then_body = [self._parse_stmt(s) for s in stmt.body]
        else_body = []

        if stmt.orelse:
            # elif → nested ast.If
            if len(stmt.orelse) == 1 and isinstance(stmt.orelse[0], ast.If):
                else_body.append(self.parse_if(stmt.orelse[0]))
            else:
                # else
                else_body = [self._parse_stmt(s) for s in stmt.orelse]

        return IRIf(condition, then_body, else_body)

    # ---------- COMPARISONS ----------

    def parse_compare(self, expr):
        if not isinstance(expr, ast.Compare):
            raise NotImplementedError("Only simple comparisons supported")

        if len(expr.ops) != 1 or len(expr.comparators) != 1:
            raise NotImplementedError("Complex comparisons not supported")

        left = self._parse_expr(expr.left)
        right = self._parse_expr(expr.comparators[0])

        op_map = {
            ast.Lt: "<",
            ast.Gt: ">",
            ast.LtE: "<=",
            ast.GtE: ">=",
            ast.Eq: "==",
            ast.NotEq: "!=",
        }

        op_type = type(expr.ops[0])
        if op_type not in op_map:
            raise NotImplementedError("Unsupported comparison operator")

        return IRCompare(left, op_map[op_type], right)
