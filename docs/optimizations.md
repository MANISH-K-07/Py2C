# Optimizations in Py2C

This document describes the **optimization passes** implemented in the Py2C compiler and explains how they operate on the Intermediate Representation (IR).

Unlike source-to-source transpilers, Py2C applies **classical compiler optimizations** at the IR level, demonstrating a real compiler pipeline suitable for academic and professional evaluation.

---

## Why Optimizations Matter

Optimizations serve multiple purposes in Py2C:

- Improve generated C code quality
- Remove unnecessary computations
- Demonstrate compiler theory knowledge
- Enable scalable future optimizations
- Strengthen academic credibility for MS / MEng applications

All optimizations operate **after parsing** and **before code generation**.

---

## Optimization Pipeline

The current optimization pipeline is:

1. **Constant Folding**
2. **Dead Code Elimination (DCE)**

Pipeline order matters:

```
Python AST
↓
IR Generation
↓
Constant Folding
↓
Dead Code Elimination
↓
C Code Generation
```


Each optimization pass is independent and composable.

---

## 1. Constant Folding

### Overview

Constant folding evaluates expressions **at compile time** when all operands are constants.

This reduces runtime computation and simplifies IR trees.

### Example

Python:

```python
x = 3 + 4 * 2
```

Before optimization:

```
IRAssign(
  x,
  IRBinOp(
    IRConst(3),
    Add,
    IRBinOp(IRConst(4), Mult, IRConst(2))
  )
)
```

After constant folding:

```
IRAssign(
  x,
  IRConst(11)
)
```

### Supported Operations

The following operations are folded:

- Addition (`Add`)
- Subtraction (`Sub`)
- Multiplication (`Mult`)
- Division (`Div`)

Only **pure integer expressions** are folded.

### Implementation Strategy

- Traverses the IR recursively
- Rewrites IRBinOp nodes when both operands are IRConst
- Preserves original structure when folding is not possible

This pass is safe, local, and deterministic.

### Benefits

- Simplifies IR trees
- Reduces generated C code complexity
- Enables further optimizations downstream

---

## 2. Dead Code Elimination (DCE)

### Overview

Dead Code Elimination removes assignments and computations whose results are never used.

This is done via **liveness analysis**.

### Example

Python:

```python
x = 10
y = 20
print(y)
```

Before DCE:

```python
x = 10
y = 20
print(y)
```

After DCE:

```python
y = 20
print(y)
```

The assignment to `x` is removed because `x` is never used.

### Liveness Analysis

DCE determines whether a variable is live (needed in the future) or dead.

Key ideas:

- Start from observable effects (e.g. `print`, loop bounds)
- Traverse statements backward
- Track variables that are required

### Root Identification

Roots of liveness include:

- Variables used in print
- Variables returned from functions
- Loop bounds and conditions
- Variables used in control flow

The analysis bootstraps from the final statement to ensure correctness.

### Loop Handling

Loops require special care:

- Loop variables are always live
- Loop bounds are always live
- Loop bodies are analyzed independently
- Dead assignments inside loops are removed safely

### Implementation Characteristics

- Backward traversal
- Conservative correctness
- No removal of control-flow structures
- Only removes provably unused assignments

### Benefits

- Smaller and cleaner C output
- Demonstrates real compiler analysis
- Preserves semantic correctness

### Optimization Safety Guarantees

Py2C optimizations are designed to be:

- Semantics-preserving
- Side-effect aware
- Deterministic
- IR-local

No optimization changes program behavior.

---

## Example: Combined Optimization

Python:

```python
x = 2 + 3
y = x * 1
z = 10
print(y)
```

Optimized:

```python
x = 5
y = x * 1
print(y)
```

---

## Why These Optimizations Matter Academically

These passes demonstrate:

- Compiler IR design
- Tree rewriting
- Data-flow analysis
- Backward liveness analysis
- Safe optimization ordering

This is well beyond a simple transpiler and aligns with coursework in:

- Compilers
- Program Analysis
- Systems
- Programming Languages

---

## Future Optimizations

Planned or possible future optimizations include:

- Common Subexpression Elimination (CSE)
- Strength Reduction
- Loop-Invariant Code Motion
- Copy Propagation
- Basic Control Flow Graph (CFG)
- SSA-based optimizations

These can be added without redesigning the IR.

---

## Summary

Py2C implements real, foundational compiler optimizations:

- **Constant Folding** for compile-time evaluation
- **Dead Code Elimination** for liveness-based cleanup

Together, they significantly improve generated code quality and demonstrate strong compiler engineering fundamentals.

This makes Py2C a credible and academically strong systems project.