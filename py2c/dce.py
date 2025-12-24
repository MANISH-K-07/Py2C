from py2c.ir import IRProgram, IRAssign, IRVar, IRBinOp, IRFor


class DeadCodeEliminator:
    def eliminate(self, ir):
        if not isinstance(ir, IRProgram):
            raise TypeError("DCE expects IRProgram")

        needed = set()

        # --- FIX: bootstrap liveness from last statement ---
        if ir.statements:
            self._mark_roots(ir.statements[-1], needed)

        new_statements = []

        for stmt in reversed(ir.statements):
            if self._is_live(stmt, needed):
                new_statements.append(stmt)

        new_statements.reverse()
        return IRProgram(new_statements)

    def _mark_roots(self, stmt, needed):
        if isinstance(stmt, IRAssign):
            needed.add(stmt.target.name)
            self._collect_vars(stmt.value, needed)

        elif isinstance(stmt, IRFor):
            needed.add(stmt.var.name)
            self._collect_vars(stmt.end, needed)
            for s in stmt.body:
                self._mark_roots(s, needed)

    def _is_live(self, stmt, needed):
        if isinstance(stmt, IRAssign):
            target = stmt.target.name

            if target not in needed:
                return False

            self._collect_vars(stmt.value, needed)
            return True

        if isinstance(stmt, IRFor):
            needed.add(stmt.var.name)
            self._collect_vars(stmt.end, needed)

            body_needed = set(needed)
            new_body = []

            for s in reversed(stmt.body):
                if self._is_live(s, body_needed):
                    new_body.append(s)

            new_body.reverse()
            stmt.body = new_body
            needed.update(body_needed)
            return True

        return True

    def _collect_vars(self, expr, needed):
        if isinstance(expr, IRVar):
            needed.add(expr.name)

        elif isinstance(expr, IRBinOp):
            self._collect_vars(expr.left, needed)
            self._collect_vars(expr.right, needed)
