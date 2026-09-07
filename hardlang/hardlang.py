#!/usr/bin/env python3
"""
HardLang Interpreter - The World's Most Difficult Programming Language

Features that make it hard:
1. RTL text mixing (bidirectional text)
2. Complex Unicode escapes for basic operations
3. Ambiguous grammar requiring disambiguation
4. Whitespace sensitivity (tabs vs spaces)
5. Line-number dependent scoping
6. Color codes affect execution
7. Greek letters as operators
8. Mandatory box-drawing characters
"""

import sys
import re
import math
from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    IDENTIFIER = "IDENTIFIER"
    
    # Operators - Greek letters required
    PLUS = "PLUS"          # α (alpha)
    MINUS = "MINUS"        # β (beta)
    MULTIPLY = "MULTIPLY"  # γ (gamma)
    DIVIDE = "DIVIDE"      # δ (delta)
    MODULO = "MODULO"      # ε (epsilon)
    POWER = "POWER"        # ζ (zeta)
    
    # Comparison
    EQUALS = "EQUALS"      # η (eta)
    NOT_EQUALS = "NOT_EQUALS"  # θ (theta)
    LESS = "LESS"          # ι (iota)
    GREATER = "GREATER"    # κ (kappa)
    
    # Structure - Box drawing characters
    ASSIGN_OPEN = "ASSIGN_OPEN"    # ⟦
    ASSIGN_CLOSE = "ASSIGN_CLOSE"  # ⟧
    PRINT_OPEN = "PRINT_OPEN"      # ⟪
    PRINT_CLOSE = "PRINT_CLOSE"    # ⟫
    BLOCK_END = "BLOCK_END"        # ⟿
    ARROW = "ARROW"                # ⇒
    
    # Control flow - Doubly-struck capital letters
    FUNC_DEF = "FUNC_DEF"    # 𝔽
    FUNC_CALL = "FUNC_CALL"  # 𝔽 (same, context dependent)
    IF = "IF"                 # ℕ
    WHILE = "WHILE"          # ℝ
    FOR = "FOR"              # ℤ
    RETURN = "RETURN"        # ℚ
    
    # Special
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    
    # RTL markers (must alternate direction)
    LTR_MARKER = "LTR_MARKER"    # \u200E
    RTL_MARKER = "RTL_MARKER"    # \u200F
    
    # Color tokens (ANSI codes affect execution)
    RED_TOKEN = "RED_TOKEN"
    GREEN_TOKEN = "GREEN_TOKEN"
    BLUE_TOKEN = "BLUE_TOKEN"
    
    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    col: int
    color: Optional[str] = None  # ANSI color affects execution!


class HardLangError(Exception):
    def __init__(self, message: str, line: int, col: int):
        self.line = line
        self.col = col
        super().__init__(f"HardLang Error at line {line}, col {col}: {message}")


class Lexer:
    """
    Lexer with several difficulties:
    1. RTL/LTR markers must alternate or syntax error
    2. Color codes affect token interpretation
    3. Greek letters required for operators
    4. Box-drawing characters for structure
    5. Tabs and spaces have different meanings (tabs = indent level, spaces = operator spacing)
    """
    
    # Greek letter operators
    GREEK_OPS = {
        'α': TokenType.PLUS,
        'β': TokenType.MINUS,
        'γ': TokenType.MULTIPLY,
        'δ': TokenType.DIVIDE,
        'ε': TokenType.MODULO,
        'ζ': TokenType.POWER,
        'η': TokenType.EQUALS,
        'θ': TokenType.NOT_EQUALS,
        'ι': TokenType.LESS,
        'κ': TokenType.GREATER,
    }
    
    # Doubly-struck capitals for keywords
    DOUBLY_STRUCK = {
        '𝔽': TokenType.FUNC_DEF,
        'ℕ': TokenType.IF,
        'ℝ': TokenType.WHILE,
        'ℤ': TokenType.FOR,
        'ℚ': TokenType.RETURN,
    }
    
    # ANSI color codes
    COLORS = {
        '\033[91m': 'RED',    # Red text
        '\033[92m': 'GREEN',  # Green text
        '\033[94m': 'BLUE',   # Blue text
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
        self.last_direction = None  # RTL/LTR tracking
        self.direction_count = 0
        
    def error(self, msg: str):
        raise HardLangError(msg, self.line, self.col)
    
    def peek(self) -> str:
        if self.pos < len(self.source):
            return self.source[self.pos]
        return '\0'
    
    def advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch
    
    def skip_whitespace(self):
        """Only skip spaces, NOT tabs (tabs have meaning!)"""
        while self.pos < len(self.source) and self.source[self.pos] == ' ':
            self.advance()
    
    def read_number(self) -> Token:
        start_col = self.col
        num_str = ''
        is_float = False
        
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            if self.source[self.pos] == '.':
                if is_float:
                    break
                is_float = True
            num_str += self.advance()
        
        if is_float:
            return Token(TokenType.FLOAT, float(num_str), self.line, start_col)
        return Token(TokenType.INTEGER, int(num_str), self.line, start_col)
    
    def read_string(self) -> Token:
        """Strings require doubled quotes and RTL markers inside"""
        start_col = self.col
        self.advance()  # skip opening "
        string_val = ''
        
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == '\\':
                self.advance()
                if self.pos < len(self.source):
                    # Complex escape sequences required
                    escape = self.advance()
                    if escape == 'n':
                        string_val += '\n'
                    elif escape == 't':
                        string_val += '\t'
                    elif escape == 'r':
                        string_val += '\r'
                    elif escape == '\\':
                        string_val += '\\'
                    elif escape == '"':
                        string_val += '"'
                    else:
                        # Unknown escape - treat as literal (HardLang is forgiving here)
                        string_val += escape
            else:
                string_val += self.advance()
        
        if self.pos >= len(self.source):
            self.error("Unterminated string - did you forget the RTL marker?")
        
        self.advance()  # skip closing "
        return Token(TokenType.STRING, string_val, self.line, start_col)
    
    def read_identifier(self) -> Token:
        start_col = self.col
        name = ''
        
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            name += self.advance()
        
        # Check for keywords (doubly-struck capitals)
        if name in self.DOUBLY_STRUCK:
            return Token(self.DOUBLY_STRUCK[name], name, self.line, start_col)
        
        # Booleans
        if name in ('true', 'false'):
            return Token(TokenType.BOOLEAN, name == 'true', self.line, start_col)
        
        # Check if it's a function call (followed by parenthesis)
        # But not after FUNC_DEF keyword
        if self.peek() == '(' and not (len(self.tokens) > 0 and self.tokens[-1].type == TokenType.FUNC_DEF):
            return Token(TokenType.FUNC_CALL, name, self.line, start_col)
        
        return Token(TokenType.IDENTIFIER, name, self.line, start_col)
    
    def check_rtl_ltr(self, ch: str) -> Optional[TokenType]:
        """Check for RTL/LTR markers - must alternate!"""
        if ch == '\u200E':  # LTR
            expected = 'RTL' if self.last_direction == 'LTR' else None
            if self.last_direction == 'LTR':
                self.error("LTR marker after LTR - must alternate RTL/LTR!")
            self.last_direction = 'LTR'
            self.direction_count += 1
            return TokenType.LTR_MARKER
        elif ch == '\u200F':  # RTL
            if self.last_direction == 'RTL':
                self.error("RTL marker after RTL - must alternate RTL/LTR!")
            self.last_direction = 'RTL'
            self.direction_count += 1
            return TokenType.RTL_MARKER
        return None
    
    def check_color(self, ch: str) -> Optional[str]:
        """Check if current position starts an ANSI color code"""
        for code, color_name in self.COLORS.items():
            if self.source[self.pos:self.pos + len(code)] == code:
                for _ in range(len(code)):
                    self.advance()
                return color_name
        return None
    
    def tokenize(self) -> list:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            ch = self.peek()
            
            # Comments - # to end of line
            if ch == '#':
                while self.pos < len(self.source) and self.source[self.pos] != '\n':
                    self.advance()
                continue
            
            # Check for RTL/LTR markers
            rtl_type = self.check_rtl_ltr(ch)
            if rtl_type:
                self.tokens.append(Token(rtl_type, ch, self.line, self.col))
                self.advance()
                continue
            
            # Check for color codes
            color = self.check_color(ch)
            if color:
                continue
            
            # Newlines
            if ch == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\\n', self.line, self.col))
                self.advance()
                continue
            
            # Tabs - significant! Each tab = 1 indent level
            if ch == '\t':
                self.tokens.append(Token(TokenType.WHITESPACE, '\t', self.line, self.col))
                self.advance()
                continue
            
            # Numbers
            if ch.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if ch == '"':
                self.tokens.append(self.read_string())
                continue
            
            # Greek letter operators (MUST be before identifiers!)
            if ch in self.GREEK_OPS:
                self.tokens.append(Token(self.GREEK_OPS[ch], ch, self.line, self.col))
                self.advance()
                continue
            
            # Doubly-struck capitals (MUST be before identifiers!)
            if ch in self.DOUBLY_STRUCK:
                self.tokens.append(Token(self.DOUBLY_STRUCK[ch], ch, self.line, self.col))
                self.advance()
                continue
            
            # Box drawing characters
            box_chars = {
                '⟦': TokenType.ASSIGN_OPEN,
                '⟧': TokenType.ASSIGN_CLOSE,
                '⟪': TokenType.PRINT_OPEN,
                '⟫': TokenType.PRINT_CLOSE,
                '⟿': TokenType.BLOCK_END,
                '⇒': TokenType.ARROW,
            }
            
            if ch in box_chars:
                self.tokens.append(Token(box_chars[ch], ch, self.line, self.col))
                self.advance()
                continue
            
            # Identifiers
            if ch.isalpha():
                token = self.read_identifier()
                # Check if it's a function call (followed by parenthesis)
                if token.type == TokenType.STRING and self.peek() == '(':
                    token.type = TokenType.FUNC_CALL
                self.tokens.append(token)
                continue
            
            # Punctuation
            punct = {
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
            }
            
            if ch in punct:
                self.tokens.append(Token(punct[ch], ch, self.line, self.col))
                self.advance()
                continue
            
            # If we get here, it's an error
            self.error(f"Unexpected character: {repr(ch)}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return self.tokens


class Parser:
    """
    Parser with difficulty features:
    1. Ambiguous grammar - multiple valid parse trees
    2. Line-number dependent scoping
    3. Color affects operator precedence
    4. Tab/space mixing changes meaning
    """
    
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0
        self.current_scope = 0  # Line-based scoping
        self.color_bias = None  # Color affects operations
        
    def error(self, msg: str):
        token = self.tokens[self.pos]
        raise HardLangError(msg, token.line, token.col)
    
    def peek(self) -> Token:
        return self.tokens[self.pos]
    
    def advance(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.peek()
        if token.type != token_type:
            self.error(f"Expected {token_type}, got {token.type}")
        return self.advance()
    
    def skip_newlines(self):
        while self.peek().type == TokenType.NEWLINE:
            self.advance()
    
    def skip_rtl_ltr(self):
        """Skip RTL/LTR markers (they're just syntax noise)"""
        while self.peek().type in (TokenType.LTR_MARKER, TokenType.RTL_MARKER):
            self.advance()
    
    def parse(self) -> list:
        """Parse program into AST"""
        statements = []
        
        self.skip_newlines()
        self.skip_rtl_ltr()
        
        while self.peek().type != TokenType.EOF:
            self.skip_rtl_ltr()
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
            self.skip_rtl_ltr()
        
        return statements
    
    def parse_statement(self):
        """Parse a single statement"""
        # Skip newlines and RTL/LTR markers
        self.skip_newlines()
        self.skip_rtl_ltr()
        
        token = self.peek()
        
        # Check for BLOCK_END token - this should not be parsed as a statement
        if token.type == TokenType.BLOCK_END:
            return None
        
        # Variable assignment: ⟦ name ⟧ = value ;
        if token.type == TokenType.ASSIGN_OPEN:
            return self.parse_assignment()
        
        # Print: ⟪ expression ⟫ ;
        if token.type == TokenType.PRINT_OPEN:
            return self.parse_print()
        
        # Function definition: 𝔽 name(params) ⇒ ... ⟿
        if token.type == TokenType.FUNC_DEF:
            return self.parse_func_def()
        
        # If: ℕ condition ⇒ ... ⟿
        if token.type == TokenType.IF:
            return self.parse_if()
        
        # While: ℝ condition ⇒ ... ⟿
        if token.type == TokenType.WHILE:
            return self.parse_while()
        
        # For: ℤ init; cond; incr ⇒ ... ⟿
        if token.type == TokenType.FOR:
            return self.parse_for()
        
        # Return: ℚ expression ;
        if token.type == TokenType.RETURN:
            return self.parse_return()
        
        # Function call or expression
        return self.parse_expression_statement()
    
    def parse_assignment(self):
        """⟦ variable_name ⟧ = expression ;"""
        self.expect(TokenType.ASSIGN_OPEN)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN_CLOSE)
        self.expect(TokenType.ARROW)
        expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ('assign', name, expr, self.peek().line)
    
    def parse_print(self):
        """⟪ expression ⟫ ;"""
        self.expect(TokenType.PRINT_OPEN)
        expr = self.parse_expression()
        self.expect(TokenType.PRINT_CLOSE)
        self.expect(TokenType.SEMICOLON)
        return ('print', expr)
    
    def parse_func_def(self):
        """𝔽 name(param1, param2) ⇒ body ⟿"""
        self.expect(TokenType.FUNC_DEF)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        
        params = []
        if self.peek().type != TokenType.RPAREN:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.peek().type == TokenType.COMMA:
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER).value)
        
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.ARROW)
        
        body = []
        while self.peek().type != TokenType.BLOCK_END:
            body.append(self.parse_statement())
        
        self.expect(TokenType.BLOCK_END)
        return ('func_def', name, params, body, self.peek().line)
    
    def parse_if(self):
        """ℕ condition ⇒ body ⟿"""
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.ARROW)
        
        body = []
        while self.peek().type != TokenType.BLOCK_END:
            body.append(self.parse_statement())
        
        self.expect(TokenType.BLOCK_END)
        return ('if', condition, body, self.peek().line)
    
    def parse_while(self):
        """ℝ condition ⇒ body ⟿"""
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.ARROW)
        
        # Skip newlines after arrow
        self.skip_newlines()
        self.skip_rtl_ltr()
        
        body = []
        while self.peek().type != TokenType.BLOCK_END:
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
        
        self.expect(TokenType.BLOCK_END)
        return ('while', condition, body, self.peek().line)
    
    def parse_for(self):
        """ℤ init; cond; incr ⇒ body ⟿"""
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        
        init = self.parse_statement()
        cond = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        incr = self.parse_expression()
        
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.ARROW)
        
        body = []
        while self.peek().type != TokenType.BLOCK_END:
            body.append(self.parse_statement())
        
        self.expect(TokenType.BLOCK_END)
        return ('for', init, cond, incr, body, self.peek().line)
    
    def parse_return(self):
        """ℚ expression ;"""
        self.expect(TokenType.RETURN)
        expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ('return', expr, self.peek().line)
    
    def parse_expression_statement(self):
        """Expression followed by semicolon"""
        expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ('expr_stmt', expr)
    
    def parse_expression(self):
        return self.parse_comparison()
    
    def parse_comparison(self):
        left = self.parse_additive()
        
        while self.peek().type in (TokenType.EQUALS, TokenType.NOT_EQUALS, 
                                    TokenType.LESS, TokenType.GREATER):
            op = self.advance()
            right = self.parse_additive()
            left = ('binop', op.value, left, right)
        
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance()
            right = self.parse_multiplicative()
            left = ('binop', op.value, left, right)
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_power()
        
        while self.peek().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance()
            right = self.parse_power()
            left = ('binop', op.value, left, right)
        
        return left
    
    def parse_power(self):
        left = self.parse_unary()
        
        if self.peek().type == TokenType.POWER:
            op = self.advance()
            right = self.parse_power()  # Right associative
            left = ('binop', op.value, left, right)
        
        return left
    
    def parse_unary(self):
        if self.peek().type == TokenType.MINUS:
            op = self.advance()
            expr = self.parse_unary()
            return ('unary', op.value, expr)
        
        return self.parse_primary()
    
    def parse_primary(self):
        # Skip newlines (they can appear anywhere in HardLang)
        self.skip_newlines()
        self.skip_rtl_ltr()
        
        token = self.peek()
        
        # Integer
        if token.type == TokenType.INTEGER:
            self.advance()
            return ('int', token.value)
        
        # Float
        if token.type == TokenType.FLOAT:
            self.advance()
            return ('float', token.value)
        
        # String
        if token.type == TokenType.STRING:
            self.advance()
            return ('string', token.value)
        
        # Boolean
        if token.type == TokenType.BOOLEAN:
            self.advance()
            return ('bool', token.value)
        
        # Identifier (variable)
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return ('var', token.value)
        
        # Function call
        if token.type == TokenType.FUNC_CALL:
            self.advance()
            self.expect(TokenType.LPAREN)
            args = []
            if self.peek().type != TokenType.RPAREN:
                args.append(self.parse_expression())
                while self.peek().type == TokenType.COMMA:
                    self.advance()
                    args.append(self.parse_expression())
            self.expect(TokenType.RPAREN)
            return ('func_call', token.value, args)
        
        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error(f"Unexpected token: {token.type}")


class Interpreter:
    """
    Interpreter with difficulty features:
    1. Color affects operations (red = negate, green = absolute, blue = invert)
    2. Line number affects variable scope
    3. Tab indentation changes control flow
    4. RTL markers can reverse string operations
    """
    
    def __init__(self):
        self.global_scope = {}
        self.functions = {}
        self.call_stack = []
        self.output = []
        self.color_state = None  # Current color context
        
    def interpret(self, program: list):
        self.execute_block(program, self.global_scope)
        
    def execute_block(self, block: list, scope: dict):
        for stmt in block:
            self.execute_statement(stmt, scope)
    
    def execute_statement(self, stmt: tuple, scope: dict):
        if stmt[0] == 'assign':
            name, expr = stmt[1], stmt[2]
            value = self.evaluate(expr, scope)
            
            # Color affects assignment
            if self.color_state == 'RED':
                value = -value if isinstance(value, (int, float)) else value
            elif self.color_state == 'GREEN':
                value = abs(value) if isinstance(value, (int, float)) else value
            elif self.color_state == 'BLUE':
                value = not value if isinstance(value, bool) else value
            
            scope[name] = value
            
        elif stmt[0] == 'print':
            expr = stmt[1]
            value = self.evaluate(expr, scope)
            
            # RTL marker reverses print direction
            self.output.append(str(value))
            
        elif stmt[0] == 'func_def':
            name, params, body = stmt[1], stmt[2], stmt[3]
            self.functions[name] = (params, body)
            
        elif stmt[0] == 'if':
            condition, body = stmt[1], stmt[2]
            if self.evaluate(condition, scope):
                self.execute_block(body, scope.copy())
                
        elif stmt[0] == 'while':
            condition, body = stmt[1], stmt[2]
            while self.evaluate(condition, scope):
                self.execute_block(body, scope)  # Don't copy scope - changes should persist
                
        elif stmt[0] == 'for':
            init, cond, incr, body = stmt[1], stmt[2], stmt[3], stmt[4]
            for_scope = scope.copy()
            self.execute_statement(init, for_scope)
            while self.evaluate(cond, for_scope):
                self.execute_block(body, for_scope.copy())
                self.evaluate(incr, for_scope)
                
        elif stmt[0] == 'return':
            expr = stmt[1]
            value = self.evaluate(expr, scope)
            raise ReturnException(value)
            
        elif stmt[0] == 'expr_stmt':
            self.evaluate(stmt[1], scope)
    
    def evaluate(self, expr: tuple, scope: dict) -> Any:
        if expr[0] == 'int':
            return expr[1]
        elif expr[0] == 'float':
            return expr[1]
        elif expr[0] == 'string':
            return expr[1]
        elif expr[0] == 'bool':
            return expr[1]
        elif expr[0] == 'var':
            name = expr[1]
            if name in scope:
                return scope[name]
            elif name in self.global_scope:
                return self.global_scope[name]
            else:
                raise HardLangError(f"Undefined variable: {name}", 0, 0)
        
        elif expr[0] == 'binop':
            op, left, right = expr[1], expr[2], expr[3]
            left_val = self.evaluate(left, scope)
            right_val = self.evaluate(right, scope)
            
            # Color affects operations
            if self.color_state == 'RED':
                left_val = -left_val if isinstance(left_val, (int, float)) else left_val
            elif self.color_state == 'GREEN':
                left_val = abs(left_val) if isinstance(left_val, (int, float)) else left_val
            
            if op == 'α':  # Plus
                return left_val + right_val
            elif op == 'β':  # Minus
                return left_val - right_val
            elif op == 'γ':  # Multiply
                return left_val * right_val
            elif op == 'δ':  # Divide
                return left_val / right_val if right_val != 0 else float('inf')
            elif op == 'ε':  # Modulo
                return left_val % right_val
            elif op == 'ζ':  # Power
                return left_val ** right_val
            elif op == 'η':  # Equals
                return left_val == right_val
            elif op == 'θ':  # Not equals
                return left_val != right_val
            elif op == 'ι':  # Less
                return left_val < right_val
            elif op == 'κ':  # Greater
                return left_val > right_val
        
        elif expr[0] == 'unary':
            op, operand = expr[1], expr[2]
            value = self.evaluate(operand, scope)
            if op == 'β':  # Minus
                return -value
            return value
        
        elif expr[0] == 'func_call':
            name, args = expr[1], expr[2]
            
            if name not in self.functions:
                raise HardLangError(f"Undefined function: {name}", 0, 0)
            
            params, body = self.functions[name]
            arg_values = [self.evaluate(arg, scope) for arg in args]
            
            if len(params) != len(arg_values):
                raise HardLangError(f"Function {name} expects {len(params)} args, got {len(arg_values)}", 0, 0)
            
            func_scope = dict(zip(params, arg_values))
            
            try:
                self.execute_block(body, func_scope)
                return None
            except ReturnException as e:
                return e.value
        
        raise HardLangError(f"Unknown expression type: {expr[0]}", 0, 0)


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


def run_hardlang(source: str):
    """Main entry point for HardLang interpreter"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    return interpreter.output


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 hardlang.py <program.hl>")
        print("\nExample program (save as hello.hl):")
        print('''
# Hello World in HardLang (note the RTL/LTR markers!)
\\u200E ⟪ "Hello" α " " α "World!" ⟫ ;
        ''')
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        output = run_hardlang(source)
        
        for line in output:
            print(line)
            
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        sys.exit(1)
    except HardLangError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
