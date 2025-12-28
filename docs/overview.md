# Py2C: Compiler Overview

Py2C is a lightweight source-to-source compiler that translates a well-defined subset of Python into equivalent C code. The project is designed to demonstrate core compiler construction principles, including parsing, intermediate representations (IR), optimization passes, and code generation.

Rather than aiming for full Python compatibility, Py2C focuses on **clarity, correctness, and extensibility**, making it suitable as an educational and research-oriented compiler project.

---

## Design Philosophy

Py2C is built around the following principles:

- **Explicit scope**: Only a restricted subset of Python is supported
- **Clear IR separation**: Parsing, optimization, and code generation are decoupled
- **Readable output**: Generated C code prioritizes clarity over micro-optimizations
- **Compiler-first mindset**: Emphasis on transformations, not transpilation hacks

This design mirrors real-world compiler pipelines such as LLVM or GCC at a simplified scale.

---

## Compilation Pipeline

The Py2C compilation process consists of four major stages:

```
Python Source
↓
Python AST (via ast module)
↓
Custom Intermediate Representation (IR)
↓
Optimization Passes
↓
C Code Generation
```


Each stage operates on a well-defined abstraction boundary.

## Stage 1: Parsing (Python AST → IR)

- Python source code is parsed using Python’s built-in `ast` module.
- The AST is traversed and lowered into a **custom IR**.
- Syntax and semantic constraints are enforced during this phase:
  - `break` / `continue` outside loops are rejected
  - `range()` step cannot be zero
  - Unsupported constructs raise explicit errors

The IR is intentionally minimal and explicit to simplify analysis and transformations.

## Stage 2: Intermediate Representation (IR)

The IR acts as a platform-independent representation of the program.

Key characteristics:
- Statement-based and expression-based nodes
- Explicit control-flow constructs (`IRIf`, `IRFor`, `IRWhile`)
- Explicit side effects (`IRAssign`, `IRPrint`)
- Simple function model (integer-only functions)

This IR is designed to be:
- Easy to analyze
- Easy to optimize
- Easy to extend

(See `docs/ir.md` for a detailed description.)

## Stage 3: Optimization Passes

Py2C includes classical compiler optimizations:

### Constant Folding
- Evaluates compile-time constant expressions
- Example:
```python
  x = 2 + 3
```
- becomes:
```python
int x = 5;
```

### Dead Code Elimination (DCE)

- Removes assignments whose results are never used
- Performs backward liveness analysis
- Handles nested loops conservatively

Optimizations operate entirely on IR, independent of source language or target language.

(See docs/optimizations.md for examples.)

## Stage 4: Code Generation (IR → C)

The final IR is lowered into ANSI C code:

- All variables are mapped to int
- Control flow maps directly to C constructs
- Python print() is lowered to printf
- Functions are emitted before main()
- Indentation and formatting prioritize readability

The generated C code is valid, readable, and suitable for compilation with standard C compilers.

---

## Scope and Intent

Py2C is not:

- A full Python compiler
- A dynamic language runtime
- A performance-optimized backend

Py2C is:

- A compiler engineering project
- A demonstration of IR-based compilation
- A foundation for future extensions (types, SSA, CFGs, etc.)

Explicit scope control is intentional and documented.

---

## Intended Audience

This project is aimed at:

- Graduate admissions reviewers (MS/MEng in CS)
- Students learning compilers and program analysis
- Developers interested in IR design and transformations

---

## Future Directions

Potential future enhancements include:

- Type inference and multi-type support
- Control Flow Graph (CFG) construction
- SSA-based IR
- Function inlining
- Loop optimizations
- Error recovery and diagnostics

These are intentionally left as extensions to preserve conceptual clarity.

---

## Summary

Py2C demonstrates how a real compiler is structured:

- Parse → IR → Optimize → Generate
- Clear abstractions
- Explicit design trade-offs
- Academically honest scope

This makes Py2C a strong, application-worthy project for advanced computer science programs.