![Koskript](https://raw.githubusercontent.com/alesisce/koskript/refs/heads/main/banner.png)

# Koskript

Koskript is a simple, embeddable, and lightweight scripting language designed to be used as a DSL inside Python applications. It features static typing, lexical scoping, and native Python interop — letting you expose any Python function or object directly to your scripts.

> **NOTE:** Koskript is currently in early development. Features like module imports, more types, and performance improvements are on the way.

---

## Features

- Static typing — `int`, `string`, `bool`, `array`, `map`
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
from koskript import KoskriptRuntime, KoskriptObject, ObjectType, ValueType, KoskriptValue

runtime = KoskriptRuntime(_globals_={
    "stdlib": KoskriptValue(ValueType.MAP, {
        "println": KoskriptObject(type=ObjectType.PYFN, value=print),
        "inputln": KoskriptObject(type=ObjectType.PYFN, value=input),
    })
})

runtime.execute(open("myscript.kos", "r").read())
```

---

## Example

```koskript
// Student grade checker
local map students = {
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

local int passing_grade = 75

foreach (string name, map data in students) {
    local int grade = data.grade

    if (grade >= passing_grade) {
        stdlib.println("PASS:", name, "->", grade)
    } elseif (grade >= 60) {
        stdlib.println("NEAR PASS:", name, "->", grade)
    } else {
        stdlib.println("FAIL:", name, "->", grade)
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
local int x = 10
local string name = "Koskript"
local bool active = true
local array items = [1, 2, 3]
local map config = { "debug": true, "version": 1 }
```

### Functions

```koskript
int fn add(int a, int b) {
    return a + b
}

local int result = add(10, 20)
```

### Control Flow

```koskript
if (x > 10) {
    stdlib.println("big")
} elseif (x == 10) {
    stdlib.println("exact")
} else {
    stdlib.println("small")
}
```

### Loops

```koskript
// while
while (x > 0) {
    x = x - 1
}

// for — iterate array
for (int item in items) {
    stdlib.println(item)
}

// foreach — iterate map
foreach (string key, int value in config) {
    stdlib.println(key, value)
}
```

### Member Access

```koskript
local map user = { "name": "Aleix", "age": 17 }
stdlib.println(user.name)
stdlib.println(user.age)
```

### Python Interop

Any Python function can be exposed to Koskript as a `PYFN`:

```python
runtime = KoskriptRuntime(_globals_={
    "stdlib": KoskriptValue(ValueType.MAP, {
        "println": KoskriptObject(type=ObjectType.PYFN, value=print),
    })
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
