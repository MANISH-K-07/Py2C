# Intermediate Representation (IR)

This document describes the **Intermediate Representation (IR)** used internally by the Py2C compiler.

The IR serves as a bridge between the Python Abstract Syntax Tree (AST) and generated C code. It is intentionally designed to be **simple, explicit, and analyzable**, enabling optimization passes such as constant folding and dead code elimination.

---

## 🎯 Design Goals

The Py2C IR is designed with the following goals:

- **Clarity**: Each IR node maps cleanly to a semantic construct
- **Simplicity**: Minimal node types, easy to reason about
- **Explicit control flow**: No implicit Python semantics
- **Optimization-friendly**: Supports static analysis and transformations
- **C-oriented**: Closely aligns with structured C constructs

The IR is *not* intended to mirror Python AST or LLVM IR exactly; instead, it occupies a pragmatic middle ground suitable for a small compiler.

---

## 🧱 IR Structure Overview

All IR nodes inherit from a common base class:

```python
class IRNode:
    pass
```

The full IR can be divided into:

- Program structure
- Statements
- Expressions
- Control flow
- Functions

---

## 📦 Program Node

### `IRProgram`

Represents the entire program.

```python
IRProgram(statements: List[IRNode])
```

- Contains a list of top-level statements
- Acts as the root of the IR tree
- Entry point for optimization and code generation

## 🧾 Statement Nodes

### `IRAssign`

Assignment statement.

```python
IRAssign(target: IRVar, value: IRExpr)
```

Example:

```python
x = 5
```

### `IRIf`

Conditional branching.

```python
IRIf(condition, then_body, else_body)
```

- `then_body` and `else_body` are lists of IR statements
- `elif` is represented as a nested `IRIf` in `else_body`

### `IRFor`

C-style `for` loop derived from Python `range()`

```python
IRFor(var, start, end, step, body)
```

Python:

```python
for i in range(0, 10, 2):
    ...
```

C:

```c
for (int i = 0; i < 10; i += 2)
```

### `IRWhile`

While loop.

```python
IRWhile(condition, body)
```

### `IRBreak` / `IRContinue`

Loop control flow.

```python
IRBreak()
IRContinue()
```

Validated to occur only inside loops.

### `IRReturn`

Function return statement.

```python
IRReturn(value)
```

All functions return `int`.

### `IRPrint`

Represents a Python `print()` call.

```python
IRPrint(values: List[IRExpr])
```

Translated into `printf` during code generation.

### `IRPass`

No-op statement.

```python
IRPass()
```

## 🔢 Expression Nodes

### `IRVar`

Variable reference.

```python
IRVar(name: str)
```

### `IRConst`

Compile-time constant.

```python
IRConst(value: int)
```

Only integer constants are supported.

### `IRBinOp`

Binary operation.

```python
IRBinOp(left, op, right)
```

Supported operators:

| Operator                  | IR Op    |
| ------------------------ | ------------ |
| +                        | Add            |
| -                        | Sub            |
| *                        | Mult           |
| /                        | Div            |
| %                        | Mod            |

### `IRCompare`

Comparison expression.

```python
IRCompare(left, op, right)
```

Supported operators:

- `<`
- `>`
- `<=`
- `>=`
- `==`
- `!=`

### `IRBoolOp`

Boolean operations.

```python
IRBoolOp(op, values)
```

- `op` is "`and`" or "`or`"
- Lowered to `&&` or `||` in C

### `IRNot`

Logical negation.

```python
IRNot(value)
```

## 🧩 Functions

### `IRFunction`

Function definition.

```python
IRFunction(name, params, body)
```

- All parameters are implicitly typed as `int`
- Functions are compiled as top-level C functions

### `IRCall`

Function call expression.

```python
IRCall(name, args)
```

Example:

```python
x = add(2, 3)
```

## 🔄 IR Example

Python:

```python
if x < 5:
    x = 3 + 4
```

IR (conceptual):

```python
IRIf(
  IRCompare(IRVar(x), "<", IRConst(5)),
  [
    IRAssign(
      IRVar(x),
      IRConst(7)
    )
  ],
  []
)
```

---

## ⚙️ Why This IR Works Well

- Enables constant folding via tree rewriting
- Enables dead code elimination via liveness analysis
- Simplifies Python semantics into structured C constructs
- Serves as a strong foundation for future CFG / SSA extensions

---

## 🔮 Future Extensions

Potential IR extensions include:

- Explicit type nodes
- Control Flow Graph (CFG)
- Static Single Assignment (SSA)
- Loop metadata
- Source location tracking

These are intentionally omitted to preserve clarity and correctness.

---

## 📌 Summary

The Py2C IR is a carefully scoped intermediate language that balances:

- Academic rigor
- Implementation simplicity
- Optimization capability
- Code generation clarity

It reflects real compiler design principles while remaining approachable and extensible.