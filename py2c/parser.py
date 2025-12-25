import ast
from py2c.ir import *


class Py2CParser:
    def __init__(self, source_code: str):
        self.tree = ast.parse(source_code)
        self.loop_depth = 0

    def parse(self):
        return IRProgram([self._parse_stmt(s) for s in self.tree.body])

    # ---------- STATEMENTS ----------

    def _parse_stmt(self, stmt):
        # Assignment
        if isinstance(stmt, ast.Assign):
            return IRAssign(
                IRVar(stmt.targets[0].id),
                self._parse_expr(stmt.value)
            )

        # Print (must come BEFORE generic call handling)
        if (
            isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Call)
            and getattr(stmt.value.func, "id", None) == "print"
        ):
            return IRPrint([self._parse_expr(a) for a in stmt.value.args])

        # Function call as statement (non-print)
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            return self._parse_expr(stmt.value)

        # For loop
        if isinstance(stmt, ast.For):
            var = IRVar(stmt.target.id)

            if not isinstance(stmt.iter, ast.Call) or stmt.iter.func.id != "range":
                raise NotImplementedError("Only range() supported")

            args = stmt.iter.args
            if len(args) == 1:
                start, end, step = IRConst(0), self._parse_expr(args[0]), IRConst(1)
            elif len(args) == 2:
                start, end, step = (
                    self._parse_expr(args[0]),
                    self._parse_expr(args[1]),
                    IRConst(1),
                )
            elif len(args) == 3:
                start, end, step = (
                    self._parse_expr(args[0]),
                    self._parse_expr(args[1]),
                    self._parse_expr(args[2]),
                )
                if isinstance(step, IRConst) and step.value == 0:
                    raise SyntaxError("range() step cannot be zero")
            else:
                raise NotImplementedError("Invalid range()")

            self.loop_depth += 1
            body = [self._parse_stmt(s) for s in stmt.body]
            self.loop_depth -= 1

            return IRFor(var, start, end, step, body)

        # While loop
        if isinstance(stmt, ast.While):
            self.loop_depth += 1
            body = [self._parse_stmt(s) for s in stmt.body]
            self.loop_depth -= 1
            return IRWhile(self._parse_expr(stmt.test), body)

        # If / Elif / Else
        if isinstance(stmt, ast.If):
            return self._parse_if(stmt)

        # Break / Continue
        if isinstance(stmt, ast.Break):
            if self.loop_depth == 0:
                raise SyntaxError("'break' outside loop")
            return IRBreak()

        if isinstance(stmt, ast.Continue):
            if self.loop_depth == 0:
                raise SyntaxError("'continue' outside loop")
            return IRContinue()

        # Function definition
        if isinstance(stmt, ast.FunctionDef):
            params = [IRVar(a.arg) for a in stmt.args.args]
            body = [self._parse_stmt(s) for s in stmt.body]
            return IRFunction(stmt.name, params, body)

        # Return
        if isinstance(stmt, ast.Return):
            return IRReturn(self._parse_expr(stmt.value))

        # Pass
        if isinstance(stmt, ast.Pass):
            return IRPass()

        raise NotImplementedError(f"Unsupported statement: {type(stmt)}")

    # ---------- EXPRESSIONS ----------

    def _parse_expr(self, expr):
        if isinstance(expr, ast.Constant):
            return IRConst(expr.value)

        if isinstance(expr, ast.Name):
            return IRVar(expr.id)

        if isinstance(expr, ast.BinOp):
            return IRBinOp(
                self._parse_expr(expr.left),
                type(expr.op).__name__,
                self._parse_expr(expr.right),
            )

        if isinstance(expr, ast.UnaryOp):
            if isinstance(expr.op, ast.USub):
                return IRBinOp(IRConst(0), "Sub", self._parse_expr(expr.operand))
            if isinstance(expr.op, ast.Not):
                return IRNot(self._parse_expr(expr.operand))
            raise NotImplementedError("Unsupported unary operator")

        if isinstance(expr, ast.Compare):
            return self._parse_compare(expr)

        if isinstance(expr, ast.BoolOp):
            op = "and" if isinstance(expr.op, ast.And) else "or"
            return IRBoolOp(op, [self._parse_expr(v) for v in expr.values])

        # Function call (expression) — print explicitly forbidden
        if isinstance(expr, ast.Call):
            if getattr(expr.func, "id", None) == "print":
                raise SyntaxError("print() cannot be used as an expression")
            return IRCall(
                expr.func.id,
                [self._parse_expr(a) for a in expr.args],
            )

        raise NotImplementedError(f"Unsupported expression: {type(expr)}")

    # ---------- HELPERS ----------

    def _parse_if(self, stmt):
        then_body = [self._parse_stmt(s) for s in stmt.body]
        else_body = []

        if stmt.orelse:
            if len(stmt.orelse) == 1 and isinstance(stmt.orelse[0], ast.If):
                else_body.append(self._parse_if(stmt.orelse[0]))
            else:
                else_body = [self._parse_stmt(s) for s in stmt.orelse]

        return IRIf(self._parse_expr(stmt.test), then_body, else_body)

    def _parse_compare(self, expr):
        op_map = {
            ast.Lt: "<",
            ast.Gt: ">",
            ast.LtE: "<=",
            ast.GtE: ">=",
            ast.Eq: "==",
            ast.NotEq: "!=",
        }
        return IRCompare(
            self._parse_expr(expr.left),
            op_map[type(expr.ops[0])],
            self._parse_expr(expr.comparators[0]),
        )
