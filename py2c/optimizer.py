from py2c.ir import (
    IRProgram,
    IRAssign,
    IRConst,
    IRBinOp,
    IRFor,
)


class ConstantFolder:
    def optimize(self, node):
        if isinstance(node, IRProgram):
            return IRProgram([self.optimize(s) for s in node.statements])

        if isinstance(node, IRAssign):
            return IRAssign(node.target, self.optimize(node.value))

        if isinstance(node, IRBinOp):
            left = self.optimize(node.left)
            right = self.optimize(node.right)

            if isinstance(left, IRConst) and isinstance(right, IRConst):
                return IRConst(self._eval(left.value, node.op, right.value))

            return IRBinOp(left, node.op, right)

        if isinstance(node, IRFor):
            return IRFor(
                node.var,
                self.optimize(node.start),
                self.optimize(node.end),
                [self.optimize(s) for s in node.body],
            )

        return node

    def _eval(self, left, op, right):
        if op == "Add":
            return left + right
        if op == "Sub":
            return left - right
        if op == "Mult":
            return left * right
        if op == "Div":
            return left / right

        raise NotImplementedError(f"Unsupported op: {op}")
