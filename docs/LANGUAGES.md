# Three Programming Languages

## Overview

This repository contains three unique programming languages:

1. **HardLang v2** - The world's hardest language (Malbolge-inspired)
2. **EasyLang v2** - The human programming language
3. **HardwareLang** - Direct hardware control language

## Language Comparison

| Feature | HardLang v2 | EasyLang v2 | HardwareLang |
|---------|-------------|-------------|--------------|
| Difficulty | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| Purpose | Obfuscated programming | General purpose | Hardware control |
| Syntax | Ternary VM code | English-like | Hardware-oriented |
| Use Case | Puzzles, challenges | Everything | Robots, IoT, embedded |
| Type System | None (raw memory) | Dynamic + inferred | Hardware types |
| Standard Library | None | Full | Hardware HAL |
| Compiler | Yes | Yes + JIT | Yes (C, ASM) |

## Quick Start

### Run EasyLang v2
```bash
python3 easylang_v2/easylang_v2.py easylang_v2/examples/calculator.el
```

### Run HardwareLang
```bash
python3 hardwarelang/hardwarelang.py hardwarelang/examples/blink.hw
```

### Compile HardwareLang to C
```bash
python3 hardwarelang/hardwarelang.py --compile-c hardwarelang/examples/blink.hw
```

## Philosophy

Each language serves a different purpose:

- **HardLang v2**: Proves that programming can be an intellectual challenge
- **EasyLang v2**: Proves that programming should be accessible to everyone
- **HardwareLang**: Proves that software can directly control the physical world
