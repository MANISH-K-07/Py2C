# Parsing in Py2C

This document explains how Py2C parses Python source code and converts it into its custom **Intermediate Representation (IR)**.

The parser forms the **front end** of the Py2C compiler pipeline and is responsible for **syntax validation, semantic structuring, and IR construction**.

---

## Parser Position in the Pipeline

```bash
Python Source Code
↓
Python AST (via ast module)
↓
Py2C Parser
↓
Intermediate Representation (IR)
```

Py2C intentionally separates **parsing** from **code generation**, mirroring real compiler architectures.

---

## Why Use Python’s `ast` Module?

Py2C leverages Python’s built-in `ast` module to:

- Avoid reimplementing Python grammar
- Rely on Python’s official syntax validation
- Focus on compiler design instead of lexer/parser boilerplate

This approach is common in research compilers and static analysis tools.

---

## Core Responsibilities of the Parser

The parser:

- Traverses Python AST nodes
- Validates supported language constructs
- Converts AST nodes into IR nodes
- Enforces semantic constraints (e.g., `break` outside loop)
- Tracks loop depth for correctness

---

## Entry Point: `Py2CParser`

```python
parser = Py2CParser(source_code)
ir = parser.parse()
```

### Responsibilities

- Parse the Python source into an AST
- Walk top-level statements
- Produce an IRProgram

---

## IRProgram Construction

Python

```python
x = 10
y = x + 5
```

IR

```bash
IRProgram([
    IRAssign(x, 10),
    IRAssign(y, x + 5)
])
```

All top-level statements are collected into a single IRProgram.

## Statement Parsing

The parser processes each AST statement via `_parse_stmt`.

Supported Statements

|Python Statement	|IR Node    |
| --------------- | --------- |
|Assignment	      |IRAssign   |
|Function Def	    |IRFunction |
|If / Elif / Else	|IRIf       |
|While Loop	      |IRWhile    |
|For Loop	        |IRFor      |
|Break	          |IRBreak    |
|Continue	        |IRContinue |
|Return	          |IRReturn   |
|Print	          |IRPrint    |
|Pass	            |IRPass     |

Unsupported statements raise `NotImplementedError`.

## Assignment Statements

Python

```python
x = a + b
```

IR

```bash
IRAssign(
    IRVar("x"),
    IRBinOp(a, Add, b)
)
```

### Rules:

- Only single-target assignments supported
- Target must be a variable name
- Tuple unpacking is intentionally unsupported

## Function Definitions

Python

```python
def add(a, b):
    return a + b
```

IR

```bash
IRFunction(
    name="add",
    params=[a, b],
    body=[IRReturn(a + b)]
)
```

### Notes:

- All parameters are positional
- No default arguments
- No keyword-only args
- Nested functions are allowed but discouraged

## If / Elif / Else Parsing

Python

```python
if x > 0:
    print(x)
elif x == 0:
    print(0)
else:
    print(-1)
```

IR Structure

```bash
IRIf(
    condition,
    then_body,
    else_body=[IRIf(...)]
)
```

### Design Choice

- `elif` is represented as a nested `IRIf` in the `else` branch
- This mirrors how many compilers lower conditionals internally

## While Loops

Python

```python
while x < 10:
    x = x + 1
```

IR

```bash
IRWhile(
    condition,
    body
)
```

The parser:

- Tracks loop depth
- Allows break and continue only inside loops

## For Loops (range Only)

Python

```python
for i in range(1, 10, 2):
    print(i)
```

IR

```bash
IRFor(
    var=i,
    start=1,
    end=10,
    step=2,
    body=[...]
)
```

## Restrictions

- Only `range()` is supported
- Valid forms:
    - range(end)
    - range(start, end)
    - range(start, end, step)
- Step value cannot be zero

Invalid constructs raise a syntax error.

## Loop Depth Tracking

The parser maintains a loop_depth counter to validate:

```
break      # ❌ invalid if loop_depth == 0
continue   # ❌ invalid if loop_depth == 0
```

This enforces semantic correctness early.

## Expression Parsing

Expressions are handled by `_parse_expr`.

Supported Expressions

|Python Expression	|IR Node        |
| ----------------- | ------------- |
|Constant	          |IRConst        |
|Variable	          |IRVar          |
|Binary Op	        |IRBinOp        |
|Unary Op	          |IRNot, IRBinOp |
|Comparison	        |IRCompare      |
|Boolean Op	        |IRBoolOp       |
|Function Call	    |IRCall         |

## Binary Operations

Python

```python
a + b
```

IR

```bash
IRBinOp(a, "Add", b)
```

Operator names come directly from Python AST node types.

## Comparisons

Python

```python
x <= y
```

IR

```bash
IRCompare(x, "<=", y)
```

Only single comparisons are supported (no chaining like `a < b < c`).

## Boolean Operations

Python

```python
a and b
```

IR

```bash
IRBoolOp("and", [a, b])
```

Supported operators:

- `and`
- `or`

## Function Calls

Python

```python
add(2, 3)
```

IR

```bash
IRCall("add", [2, 3])
```

Function calls can appear:

- As expressions
- As standalone statements

## Print Statements

Python

```python
print(x, y)
```

IR

```bash
IRPrint([x, y])
```

Print is treated as a language primitive, not a function call.

---

## Error Handling Philosophy

The parser:

- Rejects unsupported constructs early
- Raises `SyntaxError` for semantic violations
- Raises `NotImplementedError` for unsupported syntax

This keeps later stages simple and reliable.

---

## Intentional Limitations

The parser intentionally does not support:

- Classes
- Exceptions
- Lists / dicts
- Lambda functions
- List comprehensions
- Imports
- Type annotations

These choices keep Py2C focused on core compiler mechanics.

---

## Why This Parser Is Academically Strong

This parser demonstrates:

- AST-to-IR lowering
- Semantic validation
- Control-flow normalization
- Clean separation of concerns
- Compiler-style design decisions

It goes far beyond simple transpilation.

---

## Summary

The Py2C parser converts validated Python syntax into a structured, optimization-friendly IR while enforcing semantic correctness.

It forms a solid and realistic compiler front end suitable for academic evaluation and systems-focused graduate programs.