from py2c.ir import (
    IRProgram,
    IRAssign,
    IRConst,
    IRBinOp,
    IRFor,
    IRWhile,
    IRIf,
    IRReturn,
    IRPrint,
    IRCall,
    IRBoolOp,
    IRCompare,
    IRNot,
    IRFunction,
)


class ConstantFolder:
    def optimize(self, node):
        # ---------- Program ----------
        if isinstance(node, IRProgram):
            return IRProgram([self.optimize(s) for s in node.statements])

        # ---------- Assignment ----------
        if isinstance(node, IRAssign):
            return IRAssign(node.target, self.optimize(node.value))

        # ---------- Binary Operation ----------
        if isinstance(node, IRBinOp):
            left = self.optimize(node.left)
            right = self.optimize(node.right)

            if isinstance(left, IRConst) and isinstance(right, IRConst):
                return IRConst(self._eval(left.value, node.op, right.value))

            return IRBinOp(left, node.op, right)

        # ---------- For Loop ----------
        if isinstance(node, IRFor):
            return IRFor(
                node.var,
                self.optimize(node.start),
                self.optimize(node.end),
                self.optimize(node.step),
                [self.optimize(s) for s in node.body],
            )

        # ---------- While Loop ----------
        if isinstance(node, IRWhile):
            return IRWhile(
                self.optimize(node.condition),
                [self.optimize(s) for s in node.body],
            )

        # ---------- If ----------
        if isinstance(node, IRIf):
            return IRIf(
                self.optimize(node.condition),
                [self.optimize(s) for s in node.then_body],
                [self.optimize(s) for s in node.else_body],
            )

        # ---------- Function ----------
        if isinstance(node, IRFunction):
            return IRFunction(
                node.name,
                node.params,
                [self.optimize(s) for s in node.body],
            )

        # ---------- Return ----------
        if isinstance(node, IRReturn):
            return IRReturn(self.optimize(node.value))

        # ---------- Print ----------
        if isinstance(node, IRPrint):
            return IRPrint([self.optimize(v) for v in node.values])

        # ---------- Function Call ----------
        if isinstance(node, IRCall):
            return IRCall(node.name, [self.optimize(a) for a in node.args])

        # ---------- Boolean / Compare / Not ----------
        if isinstance(node, IRBoolOp):
            return IRBoolOp(node.op, [self.optimize(v) for v in node.values])

        if isinstance(node, IRCompare):
            return IRCompare(
                self.optimize(node.left),
                node.op,
                self.optimize(node.right),
            )

        if isinstance(node, IRNot):
            return IRNot(self.optimize(node.value))

        # ---------- Constants / Variables ----------
        return node

    def _eval(self, left, op, right):
        if op == "Add":
            return left + right
        if op == "Sub":
            return left - right
        if op == "Mult":
            return left * right
        if op == "Div":
            return left // right  # integer semantics
        if op == "Mod":
            return left % right

        raise NotImplementedError(f"Unsupported op: {op}")
