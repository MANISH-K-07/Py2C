# Design Decisions in Py2C

This document explains the key architectural and technical decisions behind Py2C, along with the trade-offs involved.

Py2C is intentionally designed as a **compiler project**, not a production transpiler. Every decision prioritizes **clarity, correctness, and pedagogical value**.

---

## 1. Why a Custom Intermediate Representation (IR)?

### Decision
Py2C introduces a custom IR instead of directly generating C from Python AST.

### Rationale
- Mirrors real compiler pipelines (AST → IR → Optimizations → Codegen)
- Enables optimizations like constant folding and dead code elimination
- Decouples frontend (parser) from backend (codegen)
- Makes the project extensible and academically strong

### Trade-off
- More code and complexity than direct transpilation
- Higher learning curve

This trade-off is intentional and aligns with compiler research practices.

---

## 2. Using Python’s `ast` Instead of Writing a Parser

### Decision
Use Python’s built-in `ast` module rather than implementing a lexer/parser.

### Rationale
- Python syntax correctness is guaranteed
- Eliminates grammar maintenance
- Allows focus on compiler internals
- Common approach in static analysis tools and research compilers

### Trade-off
- Limited to Python versions supported by `ast`
- Less control over parsing details

---

## 3. Minimal, Typed IR Nodes

### Decision
Each IR node represents exactly one semantic concept (e.g., `IRIf`, `IRFor`, `IRAssign`).

### Rationale
- Simplifies optimizations
- Makes transformations predictable
- Avoids ambiguous representations
- Improves readability and debugging

### Example
Instead of embedding logic in codegen:

```
IRFor(var, start, end, step, body)
```


---

## 4. Explicit Control-Flow Representation

### Decision
Loops, conditionals, `break`, and `continue` are explicit IR nodes.

### Rationale
- Enables structured control-flow analysis
- Allows semantic validation (e.g., break outside loop)
- Matches intermediate representations used in real compilers

---

## 5. Range-Based `for` Loops Only

### Decision
Only `for i in range(...)` is supported.

### Rationale
- Maps cleanly to C `for` loops
- Avoids iterator protocol complexity
- Keeps IR simple and analyzable

### Trade-off
- Python’s general iteration model is unsupported
- Sacrifices language completeness for clarity

---

## 6. Print as a Language Primitive

### Decision
Treat `print` as a primitive statement (`IRPrint`), not a function call.

### Rationale
- Allows direct lowering to `printf`
- Avoids handling Python’s I/O semantics
- Keeps C code generation clean and predictable

---

## 7. Integer-Only Type Model

### Decision
Support only `int` types.

### Rationale
- Simplifies code generation
- Avoids type inference complexity
- Matches introductory compiler IRs
- Keeps focus on control flow and optimization

### Trade-off
- No floats, strings, or complex types
- Explicitly documented as a limitation

---

## 8. Early Error Detection

### Decision
Reject unsupported or invalid constructs during parsing.

### Examples
- `break` outside loop → `SyntaxError`
- `range(..., step=0)` → `SyntaxError`
- Unsupported AST node → `NotImplementedError`

### Rationale
- Fail fast philosophy
- Keeps later phases simpler
- Improves user feedback

---

## 9. Optimization Passes as Independent Modules

### Decision
Each optimization (e.g., Constant Folding, DCE) is implemented as a standalone pass.

### Rationale
- Matches real compiler pipelines
- Enables pass ordering experiments
- Easy to extend with new optimizations

---

## 10. Readable Generated C Code

### Decision
Prioritize readable, idiomatic C over aggressive optimization.

### Rationale
- Makes output easy to inspect
- Helps users understand lowering
- Useful for teaching and debugging

### Example
```c
int x = add(2, 3);
printf("%d\n", x);
```

---

## 11. Explicit Non-Goals

Py2C does not aim to:

- Be Python-compatible
- Support full Python semantics
- Replace C compilers
- Compete with tools like Cython

This clarity strengthens the project’s academic positioning.

---

## 12. Why These Decisions Matter for Graduate Admissions

These design choices demonstrate:

- Understanding of compiler architecture
- Ability to reason about trade-offs
- Experience with IR-based optimization
- Systems-level thinking
- Clean software design

---

## Summary

Py2C’s design prioritizes compiler correctness, modularity, and educational value over feature completeness.

Every limitation is intentional, documented, and justified — exactly how strong research and systems projects are evaluated.