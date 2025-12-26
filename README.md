# Py2C — A Minimal Python-to-C Compiler

Py2C is an educational compiler project that translates a **well-defined subset of Python** into **readable, idiomatic C code**. The goal of this project is not full Python compatibility, but to demonstrate **core compiler concepts** end‑to‑end: parsing, IR construction, optimization, dead‑code elimination, and code generation.

This project is intentionally designed to be **simple, inspectable, and academically meaningful**, making it suitable as a systems/PL portfolio project.

---

## ✨ Key Features

* Python → C compilation pipeline
* Explicit Intermediate Representation (IR)
* Support for:

  * Integer variables
  * Arithmetic expressions
  * `if / elif / else`
  * `for` loops using `range()`
  * `while` loops
  * `break` / `continue`
  * Functions with integer parameters & return values
  * `print()` → `printf()` lowering
* Compiler optimizations:

  * Constant Folding
  * Dead Code Elimination (DCE)
* Clean, readable generated C code

---

## 🧠 Compiler Architecture

```
Python Source
     │
     ▼
AST (Python ast module)
     │
     ▼
Intermediate Representation (IR)
     │
     ├── Constant Folding
     ├── Dead Code Elimination
     │
     ▼
C Code Generation
```

Each phase is **explicitly separated**, making the compiler easy to extend and reason about.

---

## 📁 Project Structure

```
Py2C/
├── py2c/
│   ├── parser.py      # Python AST → IR
│   ├── ir.py          # IR node definitions
│   ├── optimizer.py   # Constant folding
│   ├── dce.py         # Dead code elimination
│   ├── codegen.py     # IR → C code generator
│   └── __init__.py
├── examples/
│   └── input.py       # Sample Python program
├── main.py            # Compiler entry point
├── README.md
└── LICENSE
```

---

## ▶️ How to Run

### 1. Write Python input

Edit the example program:

```
examples/input.py
```

### 2. Run the compiler

```bash
python main.py
```

### 3. Output

The generated C code is printed to stdout:

```c
==== Generated C Code ====

#include <stdio.h>

int add(int a, int b) {
    return (a + b);
}

int square(int x) {
    return (x * x);
}

int main() {
    int x = 5;
    int y = 40;
    int z = (x + y);
    int result = add(z, 5);
    int squared = square(result);
    if (result > 40) {
        int flag = 1;
    }
    else {
        flag = 0;
    }
    int sum = 0;
    for (int i = 0; i < 5; i += 1) {
        sum = (sum + i);
    }
    if (flag == 1) {
        printf("%d\n", squared);
    }
    else {
        printf("%d\n", result);
    }
    printf("%d\n", sum);
    return 0;
}
```

---

## 🧪 Example Input Program

```python
def add(a, b):
    return a + b

def square(x):
    return x * x

# ---- Constant Folding Demo ----
x = 2 + 3
y = 10 * 4
z = x + y

# ---- Dead Code Elimination Demo ----
unused = 999
temp = 12345  # removed by DCE

# ---- Function Calls ----
result = add(z, 5)
squared = square(result)

# ---- If / Else Demo ----
if result > 40:
    flag = 1
else:
    flag = 0

# ---- Loop Demo ----
sum = 0
for i in range(0, 5):
    sum = sum + i

# ---- Conditional Output ----
if flag == 1:
    print(squared)
else:
    print(result)

print(sum)
```

---

## 🧩 Supported Python Subset

| Feature                  | Supported    |
| ------------------------ | ------------ |
| Integers                 | ✅            |
| Arithmetic (`+ - * / %`) | ✅            |
| Variables                | ✅            |
| Functions                | ✅ (int only) |
| `if / else`              | ✅            |
| `for range()`            | ✅            |
| `while`                  | ✅            |
| `break / continue`       | ✅            |
| Lists / dicts            | ❌            |
| Classes                  | ❌            |
| Floats / strings         | ❌            |

---

## 🔬 Optimizations Implemented

### Constant Folding

Compile‑time evaluation of constant expressions:

```python
x = 2 + 3 * 4
```

Becomes:

```c
int x = 14;
```

---

### Dead Code Elimination (DCE)

Unused variable assignments are removed automatically:

```python
a = 10
b = 20
print(a)
```

`b` is eliminated during compilation.

---

## 🎓 Academic Motivation

This project was built to demonstrate:

* Understanding of **compiler pipelines**
* Experience with **ASTs and IRs**
* Basic **program analysis & optimization**
* Ability to design clean, extensible systems

It is **not** intended to be a production compiler, but a **clear and honest educational artifact**.

---

## 🚀 Future Work

* Control Flow Graph (CFG) construction
* SSA form
* Liveness analysis for registers
* Type inference
* Arrays and pointers
* Emitting `.c` files directly

---

## 📜 License

This project is open-source and available under the MIT License.

---