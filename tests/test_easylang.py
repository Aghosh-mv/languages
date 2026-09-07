#!/usr/bin/env python3
"""Tests for EasyLang v2"""

import sys
sys.path.insert(0, '../easylang_v2')

from easylang_v2 import Lexer, Parser, Interpreter, TokenType

def test_lexer():
    """Test lexer tokenization"""
    source = 'let x = 10'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.LET
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == 'x'
    assert tokens[2].type == TokenType.ASSIGN
    assert tokens[3].type == TokenType.INTEGER
    assert tokens[3].value == 10
    print("✓ Lexer test passed")

def test_parser():
    """Test parser AST generation"""
    source = 'let x = 10'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    assert len(program.statements) == 1
    assert program.statements[0].__class__.__name__ == 'Assignment'
    print("✓ Parser test passed")

def test_interpreter():
    """Test interpreter execution"""
    source = '''
let x = 10
let y = 20
let z = x + y
print z
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    assert interpreter.output[0] == '30'
    print("✓ Interpreter test passed")

def test_functions():
    """Test function definition and calling"""
    source = '''
function add(a, b)
  return a + b
end
print add(5, 3)
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    assert interpreter.output[0] == '8'
    print("✓ Function test passed")

def test_arrays():
    """Test array operations"""
    source = '''
let arr = [1, 2, 3, 4, 5]
print len(arr)
print sum(arr)
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    assert interpreter.output[0] == '5'
    assert interpreter.output[1] == '15'
    print("✓ Array test passed")

def test_control_flow():
    """Test if/else and loops"""
    source = '''
let x = 10
if x > 5
  print "big"
else
  print "small"
end
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    assert interpreter.output[0] == 'big'
    print("✓ Control flow test passed")

if __name__ == '__main__':
    test_lexer()
    test_parser()
    test_interpreter()
    test_functions()
    test_arrays()
    test_control_flow()
    print("\n✅ All tests passed!")
