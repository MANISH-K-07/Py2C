import ast
from py2c.ir import *


class Py2CParser:
    def __init__(self, source_code: str):
        self.tree = ast.parse(source_code)
        self.loop_depth = 0  # 🔹 Phase 10B: track loop nesting

    def parse(self):
        statements = []
        for stmt in self.tree.body:
            statements.append(self._parse_stmt(stmt))
        return IRProgram(statements)

    # ---------- STATEMENTS ----------

    def _parse_stmt(self, stmt):
        # ----- Assignment -----
        if isinstance(stmt, ast.Assign):
            target = stmt.targets[0].id
            value = self._parse_expr(stmt.value)
            return IRAssign(IRVar(target), value)

        # ----- For loop -----
        elif isinstance(stmt, ast.For):
            var = IRVar(stmt.target.id)

            if not isinstance(stmt.iter, ast.Call) or stmt.iter.func.id != "range":
                raise NotImplementedError("Only range() loops supported")

            args = stmt.iter.args

            if len(args) == 1:
                start = IRConst(0)
                end = self._parse_expr(args[0])
                step = IRConst(1)
            elif len(args) == 2:
                start = self._parse_expr(args[0])
                end = self._parse_expr(args[1])
                step = IRConst(1)
            elif len(args) == 3:
                start = self._parse_expr(args[0])
                end = self._parse_expr(args[1])
                step = self._parse_expr(args[2])

                # 🔹 Phase 10B: step = 0 guard
                if isinstance(step, IRConst) and step.value == 0:
                    raise SyntaxError("range() step cannot be zero")
            else:
                raise NotImplementedError("Invalid range() usage")

            self.loop_depth += 1
            body = [self._parse_stmt(s) for s in stmt.body]
            self.loop_depth -= 1

            return IRFor(var, start, end, step, body)

        # ----- While loop -----
        elif isinstance(stmt, ast.While):
            condition = self._parse_expr(stmt.test)

            self.loop_depth += 1
            body = [self._parse_stmt(s) for s in stmt.body]
            self.loop_depth -= 1

            return IRWhile(condition, body)

        # ----- If / Elif / Else -----
        elif isinstance(stmt, ast.If):
            return self.parse_if(stmt)

        # ----- Break -----
        elif isinstance(stmt, ast.Break):
            if self.loop_depth == 0:
                raise SyntaxError("'break' outside loop")
            return IRBreak()

        # ----- Continue -----
        elif isinstance(stmt, ast.Continue):
            if self.loop_depth == 0:
                raise SyntaxError("'continue' outside loop")
            return IRContinue()

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
            return IRBinOp(left, type(expr.op).__name__, right)

        if isinstance(expr, ast.UnaryOp):
            if isinstance(expr.op, ast.USub):
                return IRBinOp(IRConst(0), "Sub", self._parse_expr(expr.operand))
            if isinstance(expr.op, ast.Not):
                return IRNot(self._parse_expr(expr.operand))
            raise NotImplementedError("Unsupported unary operator")

        if isinstance(expr, ast.Compare):
            return self.parse_compare(expr)

        if isinstance(expr, ast.BoolOp):
            op = "and" if isinstance(expr.op, ast.And) else "or"
            values = [self._parse_expr(v) for v in expr.values]
            return IRBoolOp(op, values)

        raise NotImplementedError(f"Unsupported expression: {type(expr)}")

    # ---------- IF / ELIF / ELSE ----------

    def parse_if(self, stmt):
        condition = self._parse_expr(stmt.test)
        then_body = [self._parse_stmt(s) for s in stmt.body]
        else_body = []

        if stmt.orelse:
            if len(stmt.orelse) == 1 and isinstance(stmt.orelse[0], ast.If):
                else_body.append(self.parse_if(stmt.orelse[0]))
            else:
                else_body = [self._parse_stmt(s) for s in stmt.orelse]

        return IRIf(condition, then_body, else_body)

    # ---------- COMPARISONS ----------

    def parse_compare(self, expr):
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
