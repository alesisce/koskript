![Koskript](https://raw.githubusercontent.com/alesisce/koskript/refs/heads/main/banner.png)

# Koskript

Koskript is a simple, embeddable, and lightweight scripting language designed to be used as a DSL inside Python applications. It features dynamic typing, lexical scoping, and native Python interop — letting you expose any Python function or object directly to your scripts.

> **NOTE:** Koskript is currently in early development. Features like module imports, more types, and performance improvements are on the way.

---

## Features

- Dynamic typing.
- Lexical scoping with `local` declarations
- Native Python interop via `PYFN`
- `if`, `elseif`, `else`
- `while`, `for`, `foreach` loops
- Member access — `map.key.subkey`
- First-class functions with typed parameters and return types
- Embeddable in any Python application

---

## Installation

Clone the repository and import it directly into your project:

```bash
git clone https://github.com/alesisce/koskript.git
```

> PyPI package coming soon.

---

## Quick Start

```python
from koskript import KoskriptObject, KoskriptRuntime

runtime = KoskriptRuntime({
    "print": KoskriptObject(value=print)
})
runtime.execute("""
local x = 10
local y = 26

print(x+y)
""")
```

---

## Example

```koskript
// Student grade checker
local students = {
    "Aleix": {
        "age": 17,
        "grade": 95
    },
    "Maria": {
        "age": 15,
        "grade": 72
    },
    "Juan": {
        "age": 18,
        "grade": 88
    }
}

local passing_grade = 75
                   
foreach (name, data in students) {
    local grade = data.grade

    if (grade >= passing_grade) {
        print("PASS:", name, "->", grade) // Depends on how you implement it.
    } elseif (grade >= 60) {
        print("NEAR PASS:", name, "->", grade)
    } else {
        print("FAIL:", name, "->", grade)
    }
}
```

Output:
```
PASS: Aleix -> 95
NEAR PASS: Maria -> 72
PASS: Juan -> 88
```

---

## Language Reference

### Types

| Type | Description |
|------|-------------|
| `int` | Integer number |
| `string` | Text string |
| `bool` | `true` or `false` |
| `array` | Ordered list |
| `map` | Key-value store |

### Variables

```koskript
local x = 10
local name = "Koskript"
local active = true
local items = [1, 2, 3]
local config = { "debug": true, "version": 1 }
```

### Functions

```koskript
fn add(a, b) {
    return a + b
}

local result = add(10, 20)
```

### Control Flow

```koskript
if (x > 10) {
    print("big")
} elseif (x == 10) {
    print("exact")
} else {
    print("small")
}
```

### Lambda Functions

```koskript
local x = () {
    print("Hello world")
}

x()

print(() {
    print("Hello world function")
})
```

### Loops

```koskript
// while
while (x > 0) {
    x = x - 1
}

// for — iterate array
for (item in items) {
    print(item)
}

// foreach — iterate map
foreach (key, value in config) {
    print(key, value)
}
```

### Member Access

```koskript
local user = { "name": "Aleix", "age": 17 }
print(user.name)
print(user.age)
```

### Python Interop

Any Python function can be exposed to Koskript as a `KoskriptObject`:

```python
runtime = KoskriptRuntime(_globals_={
    "print": KoskriptObject(value=print)
})
```

---

## Roadmap

- [ ] Module imports (`import "mymodule"`)
- [ ] More types (`float`, `null`)
- [ ] Index access (`array[0]`, `map["key"]`)
- [ ] Performance improvements
- [ ] Standard library
- [ ] PyPI package
- [ ] Custom parser (remove Lark dependency)
- [ ] VM-based execution

---

## License

Koskript is licensed under the Mozilla Public License 2.0 (MPL-2.0).

You are free to use, modify, and redistribute Koskript. However, you may not redistribute this project under a different name or claim authorship of the Koskript language.

**Koskript is a trademark of Alesis.**

---

*Built with ❤️ by Alesis*
