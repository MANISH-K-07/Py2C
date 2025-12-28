# Code Generation in Py2C

This document explains how Py2C converts its **Intermediate Representation (IR)** into valid, readable, and idiomatic **C code**.

Unlike basic transpilers that map syntax directly, Py2C performs **IR-driven code generation**, closely resembling the back end of a real compiler.

---

## Role of the Code Generator

The code generator is the **final stage** of the Py2C pipeline:

```
Python Source
↓
Python AST
↓
Intermediate Representation (IR)
↓
Optimizations
↓
C Code Generation
```


Its responsibilities are:

- Translate IR nodes into valid C syntax
- Handle scoping and indentation
- Manage variable declarations
- Emit correct control-flow constructs
- Generate readable and maintainable output

---

## Design Philosophy

The code generator follows these principles:

- **Correctness first** – generated C must compile and run correctly
- **Readability** – output should resemble hand-written C
- **Determinism** – same IR always produces the same C code
- **Minimalism** – no unnecessary boilerplate
- **Extensibility** – easy to add new IR nodes later

---

## Entry Point: `main()`

Py2C generates a single C program with a `main()` function:

```c
int main() {
    ...
    return 0;
}
```

All top-level Python statements (except function definitions) are emitted inside main().

---

## Function Code Generation

Python

```python
def add(a, b):
    return a + b
```

Generated C

```c
int add(int a, int b) {
    return (a + b);
}
```

### Key Rules

- All functions return `int`
- All parameters are typed as `int`
- Functions are emitted before `main()`
- Function bodies are recursively generated from IR

This restriction is intentional to keep the compiler simple and focused.

## Variable Declarations

Python

```python
x = 10
x = x + 1
```

Generated C

```c
int x = 10;
x = (x + 1);
```

### Strategy

- Variables are declared on first assignment
- Subsequent assignments do not redeclare the variable
- A symbol table (`declared` set) tracks declared identifiers

This mimics real compiler symbol tracking.

## Assignment Statements

IR Node:

```
IRAssign(target, value)
```

Generated C:

```c
target = expression;
```

or (if first use):

```c
int target = expression;
```

## Expression Code Generation

Expressions are generated recursively using `_expr()`.

### Supported Expressions

|IR Node	    |    C Output Example  |
| --------- | -------------------- |
|IRConst	    |    42                |
|IRVar	      |    x                 |
|IRBinOp	    |    (a + b)           |
|IRCompare	  |    (a < b)           |
|IRBoolOp	  |    (a && b) / `(a    |
|IRNot	      |    (!x)              |
|IRCall	    |    add(2, 3)         |

Parentheses are deliberately added to preserve correctness.

## Binary Operators Mapping

| C Operator                  | IR Operator |
| ------------------------ | ------------ |
| +                        | Add            |
| -                        | Sub            |
| *                        | Mult           |
| /                        | Div            |
| %                        | Mod            |

## If / Elif / Else

Python

```python
if x > 0:
    print(x)
else:
    print(0)
```

Generated C

```c
if ((x > 0)) {
    printf("%d\n", x);
} else {
    printf("%d\n", 0);
}
```

## Implementation Notes

- `elif` is lowered into nested `else if`
- Each branch is recursively generated
- Conditions are always parenthesized

## While Loops

Python

```python
while x < 5:
    x = x + 1
```

Generated C

```c
while ((x < 5)) {
    x = (x + 1);
}
```

## For Loops (range)

Python

```python
for i in range(0, 5, 1):
    print(i)
```

Generated C

```c
for (int i = 0; i < 5; i += 1) {
    printf("%d\n", i);
}
```

### Key Properties

- Only `range()` is supported
- Loop variable is declared if needed
- Step size is respected
- Guards prevent zero-step loops

## Break and Continue

Python

```python
break
continue
```

Generated C

```c
break;
continue;
```

Semantic validation is performed during parsing.

## Print Statements

Python

```python
print(x, y)
```

Generated C

```c
printf("%d %d\n", x, y);
```

### Rules

- Uses `printf`
- Automatically builds format string
- Appends newline
- Only integer printing supported

## Function Calls

Python

```python
x = add(2, 3)
```

Generated C

```c
int x = add(2, 3);
```

Function calls work both:

- As expressions
- As standalone statements

---

## Indentation and Formatting

- 4-space indentation
- Braces on the same line
- Clean block structure
- No unnecessary whitespace

Example:

```c
if (cond) {
    ...
}
```

## Error Handling Philosophy

The code generator assumes:

- IR is valid
- Semantic errors are caught earlier
- Unsupported IR nodes raise NotImplementedError

This separation keeps responsibilities clean.

---

## Limitations (By Design)

- Only `int` type supported
- No pointers or arrays
- No structs or classes
- No memory management
- No multiple return types

These constraints keep Py2C focused on compiler fundamentals, not C complexity.

## Why This Code Generator Is Academically Strong

This implementation demonstrates:

- IR-driven back-end design
- Symbol tracking
- Structured control flow emission
- Separation of concerns
- Deterministic output generation

This is not a string-based transpiler — it is a real compiler back end.

## Future Enhancements

Potential future improvements:

- Multiple return types
- Type inference
- Function prototypes
- Header file generation
- SSA-based codegen
- Targeting other languages (LLVM IR, WASM)

---

## Summary

The Py2C code generator translates a well-defined IR into clean, idiomatic C code while preserving correctness and readability.

It completes the compiler pipeline and showcases strong understanding of compiler back-end design, making Py2C a compelling systems project.