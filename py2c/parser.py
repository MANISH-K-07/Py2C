import ast
from py2c.ir import *

class Py2CParser:
    def __init__(self, source_code: str):
        self.tree = ast.parse(source_code)
        self.loop_depth = 0

    def parse(self):
        statements = [self._parse_stmt(stmt) for stmt in self.tree.body]
        return IRProgram(statements)

    def _parse_stmt(self, stmt):
        # ----- Assignment -----
        if isinstance(stmt, ast.Assign):
            return IRAssign(IRVar(stmt.targets[0].id), self._parse_expr(stmt.value))

        # ----- For loop -----
        elif isinstance(stmt, ast.For):
            var = IRVar(stmt.target.id)
            if not isinstance(stmt.iter, ast.Call) or stmt.iter.func.id != "range":
                raise NotImplementedError("Only range() loops supported")
            args = stmt.iter.args
            if len(args) == 1:
                start, end, step = IRConst(0), self._parse_expr(args[0]), IRConst(1)
            elif len(args) == 2:
                start, end, step = self._parse_expr(args[0]), self._parse_expr(args[1]), IRConst(1)
            elif len(args) == 3:
                start, end, step = self._parse_expr(args[0]), self._parse_expr(args[1]), self._parse_expr(args[2])
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
            self.loop_depth += 1
            body = [self._parse_stmt(s) for s in stmt.body]
            self.loop_depth -= 1
            return IRWhile(self._parse_expr(stmt.test), body)

        # ----- If / Elif / Else -----
        elif isinstance(stmt, ast.If):
            return self.parse_if(stmt)

        # ----- Break / Continue -----
        elif isinstance(stmt, ast.Break):
            if self.loop_depth == 0:
                raise SyntaxError("'break' outside loop")
            return IRBreak()
        elif isinstance(stmt, ast.Continue):
            if self.loop_depth == 0:
                raise SyntaxError("'continue' outside loop")
            return IRContinue()

        # ----- Pass -----
        elif isinstance(stmt, ast.Pass):
            return IRPass()

        # ----- Print -----
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call) and getattr(stmt.value.func, "id", None) == "print":
            values = [self._parse_expr(arg) for arg in stmt.value.args]
            return IRPrint(values)

        # ----- Function / Return -----
        elif isinstance(stmt, ast.FunctionDef):
            name = stmt.name
            params = [IRVar(arg.arg) for arg in stmt.args.args]
            body = [self._parse_stmt(s) for s in stmt.body]
            return IRFunction(name, params, body)
        elif isinstance(stmt, ast.Return):
            return IRReturn(self._parse_expr(stmt.value))

        raise NotImplementedError(f"Unsupported statement: {type(stmt)}")

    # ---------- Expressions ----------
    def _parse_expr(self, expr):
        if isinstance(expr, ast.Constant):
            return IRConst(expr.value)
        if isinstance(expr, ast.Name):
            return IRVar(expr.id)
        if isinstance(expr, ast.BinOp):
            return IRBinOp(self._parse_expr(expr.left), type(expr.op).__name__, self._parse_expr(expr.right))
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
        # ----- Function Call -----
        if isinstance(expr, ast.Call):
            func_name = expr.func.id
            args = [self._parse_expr(a) for a in expr.args]
            return IRCall(func_name, args)

        raise NotImplementedError(f"Unsupported expression: {type(expr)}")

    # ---------- If / Elif / Else ----------
    def parse_if(self, stmt):
        then_body = [self._parse_stmt(s) for s in stmt.body]
        else_body = [self.parse_if(stmt.orelse[0])] if len(stmt.orelse) == 1 and isinstance(stmt.orelse[0], ast.If) else [self._parse_stmt(s) for s in stmt.orelse] if stmt.orelse else []
        return IRIf(self._parse_expr(stmt.test), then_body, else_body)

    # ---------- Comparisons ----------
    def parse_compare(self, expr):
        op_map = {ast.Lt: "<", ast.Gt: ">", ast.LtE: "<=", ast.GtE: ">=", ast.Eq: "==", ast.NotEq: "!="}
        op_type = type(expr.ops[0])
        if op_type not in op_map:
            raise NotImplementedError("Unsupported comparison operator")
        return IRCompare(self._parse_expr(expr.left), op_map[op_type], self._parse_expr(expr.comparators[0]))
