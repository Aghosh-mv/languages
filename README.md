# Two Contrasting Programming Languages

## HardLang - The World's Most Difficult Programming Language

HardLang is designed to be intentionally difficult to write while remaining Turing-complete.

### Key Difficulty Features:
1. **RTL/LTR Text Mixing**: Bidirectional text with mandatory direction changes
2. **Complex Unicode Symbols**: Greek letters for operators (α, β, γ, δ, ε, ζ, η, θ, ι, κ)
3. **Box-Drawing Characters**: ⟦ ⟧ ⟪ ⟫ ⟿ ⇒ for structure
4. **Doubly-Struck Capitals**: 𝔽 ℕ ℝ ℤ ℚ for keywords
5. **Strict Alternation**: RTL/LTR markers must alternate or syntax error
6. **Color-Coded Tokens**: ANSI codes can affect execution

### Example (Hello World):
```
# Comments use #
 ‎ ⟪ "Hello" α " " α "World!" ⟫ ;
```

### Example (Factorial):
```
 ‎ 𝔽 factorial( n ) ⇒
    ‏ ℕ n η 0 ⇒
        ‎ ℚ 1 ;
    ⟿
    ‎ ℚ n γ factorial( n β 1 ) ;
 ‏ ⟿

 ‎ ⟪ factorial( 5 ) ⟫ ;
```

---

## EasyLang - The Vibe Coding Language

EasyLang is designed to feel like vibe coding - writing code that feels natural and intuitive.

### Key Ease Features:
1. **Natural Language Syntax**: Multiple synonyms for everything
2. **Forgiving Parser**: Common typos are caught with suggestions
3. **Type Inference**: No type declarations needed
4. **Minimal Boilerplate**: Get straight to the logic
5. **Flexible Whitespace**: Newlines are optional
6. **Smart Defaults**: Everything just works

### Example (Hello World - any style works!):
```
print "Hello World!"
say "Hello World!"
output "Hello World!"
show "Hello World!"
tell "Hello World!"
```

### Example (Factorial - multiple styles):
```
# Style 1: function/end
function factorial(n)
  if n equals 0 then
    return 1
  end
  return n * factorial(n - 1)
end

# Style 2: to/done
to factorial(n)
  when n is 0
    give back 1
  done
  give back n * factorial(n - 1)
done

# Style 3: Natural language
define factorial taking n
  if n equals 0 then
    return 1
  end
  return n * factorial(n - 1)
end
```

---

## Comparison

| Feature | HardLang | EasyLang |
|---------|----------|----------|
| Learning Curve | Months | Minutes |
| Syntax | Unicode symbols | Natural language |
| Error Messages | Cryptic | Friendly with hints |
| Boilerplate | Mandatory | Optional |
| Keywords | 𝔽 ℕ ℝ ℤ ℚ | function if while for return |
| Operators | α β γ δ ε ζ η θ ι κ | + - * / % ** == != < > |
| Structure | ⟦ ⟧ ⟪ ⟫ ⟿ ⇒ | { } ( ) ; |
| RTL/LTR Required | Yes | No |

---

## Running the Languages

### HardLang:
```bash
cd languages
python3 hardlang/hardlang.py hardlang/examples/hello.hl
python3 hardlang/hardlang.py hardlang/examples/factorial.hl
python3 hardlang/hardlang.py hardlang/examples/fibonacci.hl
```

### EasyLang:
```bash
cd languages
python3 easylang/easylang.py easylang/examples/hello.el
python3 easylang/easylang.py easylang/examples/factorial.el
python3 easylang/easylang.py easylang/examples/fibonacci.el
python3 easylang/easylang.py easylang/examples/showcase.el
```

---

## Design Philosophy

**HardLang**: "Programming should be an intellectual challenge. If it's easy, you're not learning."

**EasyLang**: "Programming should be accessible. The computer should adapt to humans, not the other way around."
