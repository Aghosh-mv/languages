# EasyLang v2 - The Human Programming Language

## Philosophy
EasyLang v2 is a **real programming language** that reads like English.
Not just vibe coding - it has:

1. **Full Type System**: Inferred types with optional annotations
2. **First-Class Functions**: Lambdas, closures, higher-order functions
3. **Module System**: Import/export, packages, namespaces
4. **Standard Library**: IO, math, strings, collections, networking
5. **Error Handling**: Try/catch with pattern matching
6. **Concurrency**: Async/await, channels, goroutines
7. **Memory Management**: Automatic garbage collection
8. **Just-in-Time Compilation**: Optimized at runtime
9. **Foreign Function Interface**: Call C, Python, JavaScript
10. **REPL**: Interactive development environment

## Quick Reference

### Types (inferred or explicit)
```
let x = 10          # int
let y = 3.14        # float
let s = "hello"     # string
let b = true        # bool
let a = [1, 2, 3]  # array
let m = {a: 1}     # map
```

### Functions
```
function add(a, b)
  return a + b
end

# Or with type annotations
function multiply(a: int, b: int): int
  return a * b
end

# Lambda
let square = (x) -> x * x
```

### Control Flow
```
if x > 0 then
  print "positive"
else if x < 0 then
  print "negative"
else
  print "zero"
end

# Pattern matching
match x
  when 0: print "zero"
  when 1: print "one"
  else: print "other"
end

# Loops
for i in range(10)
  print i
end

while x > 0
  x -= 1
end
```

### Modules
```
# math.el
export function add(a, b)
  return a + b
end

# main.el
import math
print math.add(1, 2)
```

## Running
```bash
python3 easylang_v2.py program.el
# Or compile to bytecode
python3 easylang_v2.py --compile program.el
```

## Difficulty Level
⭐ (1/10) - Designed for humans
