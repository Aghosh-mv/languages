# HardLang - The World's Most Difficult Programming Language

## Philosophy
HardLang is designed to be intentionally difficult to write while remaining Turing-complete. It achieves this through:

1. **RTL Text Mixing**: Bidirectional text with mandatory direction changes
2. **Complex Escape Sequences**: 5+ character escapes for common operations
3. **Mandatory Obfuscation**: Unicode box-drawing characters as syntax
4. **Ambiguous Grammar**: Multiple valid parse trees for same input
5. **Mathematical Notation**: Greek letters and symbols for operators
6. **Color-Coded Tokens**: ANSI color codes affect execution
7. **Whitespace Sensitivity**: Tabs and spaces have different meanings
8. **Line Number Dependencies**: Line numbers affect variable scoping

## Quick Reference

### Variables
```
⟦ variable_name ⟧ = value ;
```

### Control Flow
```
 doubly-struck-capital-n  condition ⇒
   body ⟿
 doubly-struck-capital-n  
```

### Functions
```
 doubly-struck-capital-f  name( param_1 , param_2 ) ⇒
   return_value ⟿
```

### Output
```
 ⟪ expression ⟫ ;
```

## Running
```bash
python3 hardlang.py program.hl
```
