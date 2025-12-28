# Limitations and Future Work

This document outlines the current limitations of Py2C and presents a structured roadmap for future enhancements.

Py2C is intentionally scoped as an educational compiler project. Many limitations are **design decisions**, not shortcomings.

---

## 1. Language Coverage Limitations

### Current Limitations
- Only integer (`int`) types are supported
- No floating-point, string, or boolean types
- No Python collections (list, tuple, dict, set)
- No user-defined classes or objects
- No exception handling (`try/except`)
- No dynamic typing

### Rationale
Supporting these features would significantly complicate:
- Type inference
- Memory layout
- Runtime semantics
- Code generation

The current design prioritizes **clarity and correctness**.

---

## 2. Function Support Constraints

### Current Limitations
- Only `int`-returning functions are supported
- No recursion
- No function overloading
- No default arguments
- No keyword arguments

### Future Work
- Extend IR with function signatures and return types
- Add stack frame modeling
- Enable recursive calls
- Introduce simple calling conventions

---

## 3. Control Flow Limitations

### Current Limitations
- `for` loops restricted to `range(...)`
- No `else` clause for loops
- No `break`/`continue` labels
- No short-circuit lowering for complex boolean expressions

### Future Work
- Support iterator-based loops
- Lower control flow into basic blocks
- Introduce CFG-based IR

---

## 4. Type System Limitations

### Current Limitations
- Implicit integer typing only
- No type inference
- No type checking beyond basic correctness

### Future Work
- Introduce a static type checker
- Add explicit IR types
- Support mixed-type expressions
- Implement type promotion rules

---

## 5. Optimization Limitations

### Current Limitations
- Constant folding is local and expression-level
- Dead code elimination is intraprocedural
- No data-flow analysis
- No loop optimizations

### Future Work
- Control-flow graph (CFG) construction
- Liveness analysis
- Loop-invariant code motion
- Strength reduction
- Common subexpression elimination (CSE)
- Interprocedural optimization

---

## 6. Memory and Runtime Model

### Current Limitations
- No heap allocation
- No pointer semantics
- No reference counting or garbage collection

### Future Work
- Introduce explicit memory model
- Stack vs heap allocation
- Simple reference semantics
- Escape analysis

---

## 7. Code Generation Constraints

### Current Limitations
- Only C is supported as a target language
- No platform-specific optimizations
- No ABI awareness
- No debug symbols

### Future Work
- LLVM IR backend
- WASM code generation
- Multi-target backend abstraction
- Debug information generation

---

## 8. Error Reporting Limitations

### Current Limitations
- Errors reported during parsing only
- No source location mapping
- No structured diagnostics

### Future Work
- Line/column tracking
- Diagnostic categories
- Compiler-style error messages
- Warning system

---

## 9. Testing and Validation

### Current Limitations
- Minimal automated testing
- No property-based testing
- No differential testing against CPython

### Future Work
- Golden output tests
- Randomized AST testing
- Cross-validation with C execution
- Continuous integration setup

---

## 10. Performance Limitations

### Current Limitations
- No performance benchmarking
- No optimization tuning
- No profiling

### Future Work
- Benchmark suite
- Optimization effectiveness evaluation
- Performance vs readability trade-offs

---

## 11. Scalability Limitations

### Current Limitations
- Designed for small programs
- No module system
- No separate compilation

### Future Work
- Multi-file support
- Symbol tables
- Incremental compilation
- Dependency tracking

---

## 12. Research and Academic Extensions

Potential extensions suitable for research projects:
- SSA-based IR
- Formal verification of transformations
- Program equivalence checking
- Static analysis (taint, aliasing)
- Compiler correctness proofs

---

## Summary

Py2C is intentionally minimal but architecturally complete.

Its limitations reflect **conscious design trade-offs**, while its future roadmap demonstrates:
- Systems thinking
- Compiler theory understanding
- Research readiness
- Engineering maturity

This makes Py2C a strong foundation for advanced academic or research-oriented extensions.
