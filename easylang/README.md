# EasyLang - The Vibe Coding Language

## Philosophy
EasyLang is designed to feel like vibe coding - writing code that feels natural and intuitive. It's still a real programming language, but with these features:

1. **Natural Language Syntax**: Write code like you're talking to a friend
2. **Forgiving Parser**: Multiple ways to write the same thing
3. **Type Inference**: No need to declare types
4. **Minimal Boilerplate**: Get straight to the logic
5. **Smart Defaults**: Everything just works out of the box
6. **Friendly Errors**: Messages that help you fix problems
7. **Multiple Styles**: Choose what feels right for you
8. **Auto-Complete Hints**: Suggestions as you type

## Quick Reference

### Variables (any of these work!)
```
let x = 5
x = 10
x is now 10
set x to 10
make x equal 10
```

### Output
```
print "Hello World"
say "Hello World"
output "Hello World"
console.log "Hello World"
show x
tell me x
```

### Control Flow (all equivalent)
```
if x > 5 then do
  print "big"
end

when x > 5
  print "big"
done

whenever x is greater than 5
  print "big"
close

if x > 5: print "big"
```

### Loops
```
repeat 10 times
  print "hello"
end

do this 10 times
  print "hello"
done

for 10 iterations
  print "hello"
end

loop 10x
  print "hello"
end
```

### Functions
```
to greet name do
  print "Hello " + name
end

function greet(name) {
  print "Hello " + name
}

define greet taking name {
  print "Hello " + name
}
```

## Running
```bash
python3 easylang.py program.el
```
