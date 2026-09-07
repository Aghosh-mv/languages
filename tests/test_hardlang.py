#!/usr/bin/env python3
"""Tests for HardLang"""

import sys
sys.path.insert(0, '../hardlang')

from hardlang import Lexer, Parser, Interpreter

def test_hello_world():
    """Test hello world program"""
    source = '''
# Hello World
 ‎ ⟪ "Hello" α " " α "World!" ⟫ ;
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    assert "Hello World!" in interpreter.output
    print("✓ Hello World test passed")

def test_factorial():
    """Test factorial program"""
    source = '''
# Factorial function
 ‎ 𝔽 factorial( n ) ⇒
    ‏ ℕ n η 0 ⇒
        ‎ ℚ 1 ;
    ⟿
    ‎ ℚ n γ factorial( n β 1 ) ;
 ‏ ⟿

 ‎ ⟪ factorial( 5 ) ⟫ ;
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    assert "120" in interpreter.output
    print("✓ Factorial test passed")

def test_fibonacci():
    """Test fibonacci program"""
    source = '''
# Fibonacci function
 ‎ 𝔽 fibonacci( n ) ⇒
    ‏ ℕ n η 0 ⇒
        ‎ ℚ 0 ;
    ‏ ℕ n η 1 ⇒
        ‎ ℚ 1 ;
    ⟿
    ‎ ℚ fibonacci( n β 1 ) γ fibonacci( n β 2 ) ;
 ‏ ⟿

 ‎ ⟪ fibonacci( 10 ) ⟫ ;
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    assert "55" in interpreter.output
    print("✓ Fibonacci test passed")

if __name__ == '__main__':
    test_hello_world()
    test_factorial()
    test_fibonacci()
    print("\n✅ All HardLang tests passed!")
