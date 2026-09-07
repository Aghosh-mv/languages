# EasyLang - The Vibe Coding Language

EasyLang is designed to feel like vibe coding - writing code that feels natural and intuitive.

## Key Features

### 1. Natural Language Syntax
Multiple synonyms for everything:
```
print "Hello World!"
say "Hello World!"
output "Hello World!"
show "Hello World!"
tell "Hello World!"
```

### 2. Forgiving Parser
Common typos are caught with suggestions:
```
# If you type "fucntion" instead of "function"
# EasyLang will suggest: "Did you mean 'function'?"
```

### 3. Type Inference
No type declarations needed:
```
let x = 10          # Automatically inferred as integer
let name = "Alice"  # Automatically inferred as string
let arr = [1, 2, 3] # Automatically inferred as array
```

### 4. Minimal Boilerplate
Get straight to the logic:
```
# No imports needed
# No class definitions needed
# Just write your code
```

### 5. Flexible Whitespace
Newlines are optional:
```
let x = 10; let y = 20; print x + y
```

### 6. Smart Defaults
Everything just works:
```
# Arrays auto-resize
let arr = []
arr.push(1)
arr.push(2)

# Strings are mutable
let name = "Alice"
name.upper()  # Returns "ALICE"
```

## Syntax

### Variables
```
let x = 10
const PI = 3.14159
```

### Functions
```
function add(a, b) then
  return a + b
end

# Lambda
let square = (x) -> x * x
```

### Control Flow
```
if condition then
  # do something
else
  # do something else
end

for i in range(10)
  print i
end

while true
  print "infinite loop"
end
```

### Arrays
```
let arr = [1, 2, 3, 4, 5]
print len(arr)  # 5
print sum(arr)  # 15
print max(arr)  # 5
print min(arr)  # 1
```

### Maps
```
let person = {name: "Alice", age: 30}
print person.name  # Alice
```

### Error Handling
```
try
  let result = 10 / 0
catch error
  print "Error:", error
finally
  print "Cleanup"
end
```

## Running

```bash
python easylang/easylang.py easylang/examples/hello.el
```

## Examples

See the `examples/` directory for more examples.
