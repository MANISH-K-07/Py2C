from py2c.ir import *


class DeadCodeEliminator:
    def eliminate(self, ir: IRProgram) -> IRProgram:
        if not isinstance(ir, IRProgram):
            raise TypeError("DCE expects IRProgram")

        live = set()
        new_statements = []

        # Step 1: mark roots (side-effect statements)
        for stmt in ir.statements:
            if self._has_side_effect(stmt):
                self._mark_used(stmt, live)

        # Step 2: backward sweep
        for stmt in reversed(ir.statements):
            if isinstance(stmt, IRAssign):
                target = stmt.target.name
                used = self._used_vars(stmt.value)

                if target in live:
                    live.remove(target)
                    live |= used
                    new_statements.append(stmt)
                # else: dead assignment → dropped

            else:
                # keep all non-assign statements
                self._mark_used(stmt, live)
                new_statements.append(stmt)

        new_statements.reverse()
        return IRProgram(new_statements)

    # ---------- Helpers ----------

    def _has_side_effect(self, stmt):
        return isinstance(
            stmt,
            (IRPrint, IRReturn, IRCall, IRBreak, IRContinue)
        )

    def _mark_used(self, stmt, live):
        for v in self._used_vars(stmt):
            live.add(v)

        if isinstance(stmt, IRFor):
            live.add(stmt.var.name)
            for s in stmt.body:
                self._mark_used(s, live)

        if isinstance(stmt, IRWhile):
            self._mark_used(stmt.condition, live)
            for s in stmt.body:
                self._mark_used(s, live)

        if isinstance(stmt, IRIf):
            self._mark_used(stmt.condition, live)
            for s in stmt.then_body:
                self._mark_used(s, live)
            for s in stmt.else_body:
                self._mark_used(s, live)

        if isinstance(stmt, IRFunction):
            for s in stmt.body:
                self._mark_used(s, live)

    def _used_vars(self, node):
        used = set()

        def visit(n):
            if isinstance(n, IRVar):
                used.add(n.name)
            elif isinstance(n, IRBinOp):
                visit(n.left)
                visit(n.right)
            elif isinstance(n, IRCompare):
                visit(n.left)
                visit(n.right)
            elif isinstance(n, IRBoolOp):
                for v in n.values:
                    visit(v)
            elif isinstance(n, IRNot):
                visit(n.value)
            elif isinstance(n, IRCall):
                for a in n.args:
                    visit(a)
            elif isinstance(n, IRReturn):
                visit(n.value)
            elif isinstance(n, IRPrint):
                for v in n.values:
                    visit(v)

        visit(node)
        return used
