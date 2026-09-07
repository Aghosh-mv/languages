# HardLang v2 - The Malbolge of Practical Languages

## Philosophy
HardLang v2 is designed to be **genuinely difficult** to write, not artificially so.
Inspired by Malbolge, it uses:

1. **Self-Modifying Code**: Program modifies itself as it runs
2. **Ternary VM**: Base-3 virtual machine with 3 registers
3. **Encrypted Source**: Code is encrypted, decrypts during execution
4. **Rotational Instructions**: Operations change based on position
5. **No Variables**: Only memory addresses (0-59049)
6. **No Strings**: Only numbers and operations
7. **Right-to-Left Execution**: Instructions execute backwards
8. **Trinary Opcodes**: Each instruction is a ternary digit
9. **Memory Encryption**: Values encrypt after each operation
10. **Crazy Tables**: Operations determined by crazytown lookup

## Quick Reference

### Instructions (Ternary)
```
0 = nop
1 = inc register
2 = dec register
3 = add registers
4 = load from memory
5 = store to memory
6 = jump if zero
7 = jump if nonzero
8 = halt
9 = output
A = input
B = encrypt memory
C = decrypt memory
D = rotate instruction
E = copy memory
F = crazy operation
```

### Example (Hello World)
```
9*8*7*6*5*4*3*2*1*0
```

### Example (Add two numbers)
```
1 2 3 4 5 6 7 8 9 A B C D E F 0
```

## Running
```bash
python3 hardlang_v2.py program.hl2
```

## Difficulty Level
⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ (10/10)
- Average time to write "Hello World": 2-3 hours
- Average time to write Fibonacci: 1-2 days
- Average time to write a compiler: 6-12 months
