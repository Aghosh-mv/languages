#!/usr/bin/env python3
"""
EasyLang Interpreter - The Vibe Coding Language

Features that make it easy:
1. Natural language syntax (multiple ways to write everything)
2. Forgiving parser (handles common mistakes)
3. Type inference (no type declarations needed)
4. Minimal boilerplate
5. Friendly error messages
6. Multiple syntax styles supported
7. Auto-complete hints
8. Smart defaults
"""

import sys
import re
import math
from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, List


class TokenType(Enum):
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    IDENTIFIER = "IDENTIFIER"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    POWER = "POWER"
    
    # Comparison
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    LESS = "LESS"
    GREATER = "GREATER"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    # Assignment
    ASSIGN = "ASSIGN"
    PLUS_ASSIGN = "PLUS_ASSIGN"
    MINUS_ASSIGN = "MINUS_ASSIGN"
    
    # Keywords (natural language friendly)
    LET = "LET"
    PRINT = "PRINT"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    END = "END"
    DO = "DO"
    REPEAT = "REPEAT"
    TIMES = "TIMES"
    WHILE = "WHILE"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # Punctuation
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    NEWLINE = "NEWLINE"
    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    col: int


class EasyLangError(Exception):
    def __init__(self, message: str, line: int, col: int):
        self.line = line
        self.col = col
        super().__init__(f"EasyLang Error at line {line}, col {col}: {message}")


class Lexer:
    """
    Forgiving lexer that handles:
    - Multiple keyword variations
    - Common typos
    - Flexible whitespace
    - Natural language operators
    """
    
    # Natural language keywords (multiple synonyms for everything!)
    KEYWORDS = {
        'let': TokenType.LET,
        'set': TokenType.LET,
        'make': TokenType.LET,
        'assign': TokenType.LET,
        'create': TokenType.LET,
        
        # Assignment synonyms
        'now': TokenType.LET,
        'gets': TokenType.LET,
        'equal': TokenType.LET,
        'equals': TokenType.EQUALS,
        
        'print': TokenType.PRINT,
        'say': TokenType.PRINT,
        'output': TokenType.PRINT,
        'show': TokenType.PRINT,
        'tell': TokenType.PRINT,
        'display': TokenType.PRINT,
        'write': TokenType.PRINT,
        'echo': TokenType.PRINT,
        
        'if': TokenType.IF,
        'when': TokenType.IF,
        'whenever': TokenType.IF,
        'assuming': TokenType.IF,
        'given': TokenType.IF,
        
        'then': TokenType.THEN,
        'do': TokenType.DO,
        'proceed': TokenType.THEN,
        'continue': TokenType.THEN,
        
        'else': TokenType.ELSE,
        'otherwise': TokenType.ELSE,
        'if not': TokenType.ELSE,
        
        'end': TokenType.END,
        'done': TokenType.END,
        'finished': TokenType.END,
        'close': TokenType.END,
        'stop': TokenType.END,
        
        'repeat': TokenType.REPEAT,
        'loop': TokenType.REPEAT,
        'iterate': TokenType.REPEAT,
        'again': TokenType.REPEAT,
        
        'iterations': TokenType.TIMES,
        'rounds': TokenType.TIMES,
        
        'while': TokenType.WHILE,
        'until': TokenType.WHILE,
        'as long as': TokenType.WHILE,
        
        'function': TokenType.FUNCTION,
        'func': TokenType.FUNCTION,
        'def': TokenType.FUNCTION,
        'define': TokenType.FUNCTION,
        'to': TokenType.FUNCTION,
        'method': TokenType.FUNCTION,
        
        # Power operator
        'to the power of': TokenType.POWER,
        'raised to': TokenType.POWER,
        
        'return': TokenType.RETURN,
        'give back': TokenType.RETURN,
        'send back': TokenType.RETURN,
        
        'and': TokenType.AND,
        'also': TokenType.AND,
        'plus': TokenType.AND,
        'with': TokenType.AND,
        
        'or': TokenType.OR,
        'either': TokenType.OR,
        'otherwise': TokenType.OR,
        
        'not': TokenType.NOT,
        'no': TokenType.NOT,
        'isnt': TokenType.NOT,
        'is not': TokenType.NOT,
        'aint': TokenType.NOT,
        
        # Comparison operators as keywords
        'equals': TokenType.EQUALS,
        'is equal to': TokenType.EQUALS,
        'is': TokenType.EQUALS,
        'same as': TokenType.EQUALS,
        'not equal to': TokenType.NOT_EQUALS,
        'differs from': TokenType.NOT_EQUALS,
        'less than': TokenType.LESS,
        'smaller than': TokenType.LESS,
        'under': TokenType.LESS,
        'below': TokenType.LESS,
        'greater than': TokenType.GREATER,
        'bigger than': TokenType.GREATER,
        'over': TokenType.GREATER,
        'above': TokenType.GREATER,
        'less than or equal to': TokenType.LESS_EQUAL,
        'at most': TokenType.LESS_EQUAL,
        'no more than': TokenType.LESS_EQUAL,
        'greater than or equal to': TokenType.GREATER_EQUAL,
        'at least': TokenType.GREATER_EQUAL,
        'no less than': TokenType.GREATER_EQUAL,
    }
    
    # Operator synonyms
    OPERATORS = {
        '+': TokenType.PLUS,
        'plus': TokenType.PLUS,
        'add': TokenType.PLUS,
        'and': TokenType.PLUS,
        
        '-': TokenType.MINUS,
        'minus': TokenType.MINUS,
        'subtract': TokenType.MINUS,
        'take away': TokenType.MINUS,
        
        '*': TokenType.MULTIPLY,
        'times': TokenType.MULTIPLY,
        'multiply': TokenType.MULTIPLY,
        'multiplied by': TokenType.MULTIPLY,
        
        '/': TokenType.DIVIDE,
        'divided by': TokenType.DIVIDE,
        'divide': TokenType.DIVIDE,
        'over': TokenType.DIVIDE,
        
        '%': TokenType.MODULO,
        'mod': TokenType.MODULO,
        'modulo': TokenType.MODULO,
        'remainder': TokenType.MODULO,
        
        '**': TokenType.POWER,
        'power': TokenType.POWER,
        'to the power of': TokenType.POWER,
        'raised to': TokenType.POWER,
        
        '=': TokenType.EQUALS,
        '==': TokenType.EQUALS,
        'equals': TokenType.EQUALS,
        'is equal to': TokenType.EQUALS,
        'is': TokenType.EQUALS,
        'same as': TokenType.EQUALS,
        
        '!=': TokenType.NOT_EQUALS,
        'is not equal to': TokenType.NOT_EQUALS,
        'not equal to': TokenType.NOT_EQUALS,
        'differs from': TokenType.NOT_EQUALS,
        
        '<': TokenType.LESS,
        'less than': TokenType.LESS,
        'smaller than': TokenType.LESS,
        'under': TokenType.LESS,
        'below': TokenType.LESS,
        
        '>': TokenType.GREATER,
        'greater than': TokenType.GREATER,
        'bigger than': TokenType.GREATER,
        'over': TokenType.GREATER,
        'above': TokenType.GREATER,
        
        '<=': TokenType.LESS_EQUAL,
        'less than or equal to': TokenType.LESS_EQUAL,
        'at most': TokenType.LESS_EQUAL,
        'no more than': TokenType.LESS_EQUAL,
        
        '>=': TokenType.GREATER_EQUAL,
        'greater than or equal to': TokenType.GREATER_EQUAL,
        'at least': TokenType.GREATER_EQUAL,
        'no less than': TokenType.GREATER_EQUAL,
        
        '=': TokenType.ASSIGN,
        ':=': TokenType.ASSIGN,
        'gets': TokenType.ASSIGN,
        'is now': TokenType.ASSIGN,
        'becomes': TokenType.ASSIGN,
        
        '+=': TokenType.PLUS_ASSIGN,
        'plus equals': TokenType.PLUS_ASSIGN,
        'increment by': TokenType.PLUS_ASSIGN,
        
        '-=': TokenType.MINUS_ASSIGN,
        'minus equals': TokenType.MINUS_ASSIGN,
        'decrement by': TokenType.MINUS_ASSIGN,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
        
    def error(self, msg: str):
        # Friendly error messages!
        friendly_msg = msg
        if "unexpected" in msg.lower():
            friendly_msg = f"Hmm, I didn't expect that here. {msg}"
        elif "expected" in msg.lower():
            friendly_msg = f"I was looking for something else. {msg}"
        raise EasyLangError(friendly_msg, self.line, self.col)
    
    def peek(self) -> str:
        if self.pos < len(self.source):
            return self.source[self.pos]
        return '\0'
    
    def peek_word(self) -> str:
        """Peek at the next word (for multi-word keywords)"""
        pos = self.pos
        while pos < len(self.source) and self.source[pos] in ' \t':
            pos += 1
        word = ''
        while pos < len(self.source) and self.source[pos] not in ' \t\n\r':
            word += self.source[pos]
            pos += 1
        return word.lower()
    
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
        while self.pos < len(self.source) and self.source[self.pos] in ' \t':
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
        start_col = self.col
        quote_char = self.peek()
        self.advance()  # skip opening quote
        
        string_val = ''
        while self.pos < len(self.source) and self.source[self.pos] != quote_char:
            if self.source[self.pos] == '\\':
                self.advance()
                if self.pos < len(self.source):
                    escape = self.advance()
                    escape_chars = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                    string_val += escape_chars.get(escape, escape)
            else:
                string_val += self.advance()
        
        if self.pos >= len(self.source):
            self.error("Unterminated string - you forgot to close it!")
        
        self.advance()  # skip closing quote
        return Token(TokenType.STRING, string_val, self.line, start_col)
    
    def read_identifier(self) -> Token:
        start_col = self.col
        name = ''
        
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            name += self.advance()
        
        name_lower = name.lower()
        
        # Check for single-word keywords
        if name_lower in self.KEYWORDS:
            # First, try to match multi-word keywords that start with this word
            # Save position
            saved_pos = self.pos
            saved_col = self.col
            saved_line = self.line
            
            # Try to match multi-word keywords
            for keyword in self.KEYWORDS:
                if ' ' in keyword and keyword.startswith(name_lower):
                    # Try to match the rest of the keyword
                    parts = keyword.split(' ')
                    matched = True
                    for part in parts[1:]:
                        self.skip_whitespace()
                        word = self.peek_word()
                        if word == part:
                            # Consume the word
                            for _ in range(len(word)):
                                self.advance()
                            self.skip_whitespace()
                        else:
                            matched = False
                            break
                    
                    if matched:
                        return Token(self.KEYWORDS[keyword], keyword, self.line, start_col)
                    
                    # Reset position if no match
                    self.pos = saved_pos
                    self.col = saved_col
                    self.line = saved_line
            
            # No multi-word keyword matched, return single-word keyword
            return Token(self.KEYWORDS[name_lower], name, self.line, start_col)
        
        # Check for common typos and suggest corrections
        if name_lower == 'ture':
            self.error("Did you mean 'true'?")
        elif name_lower == 'flase':
            self.error("Did you mean 'false'?")
        elif name_lower == 'pritn':
            self.error("Did you mean 'print'?")
        elif name_lower == 'fuction':
            self.error("Did you mean 'function'?")
        
        # Booleans
        if name_lower in ('true', 'yes', 'yep', 'yeah', '1', 'on'):
            return Token(TokenType.BOOLEAN, True, self.line, start_col)
        if name_lower in ('false', 'no', 'nope', 'nah', '0', 'off'):
            return Token(TokenType.BOOLEAN, False, self.line, start_col)
        
        return Token(TokenType.IDENTIFIER, name, self.line, start_col)
    
    def tokenize(self) -> list:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            ch = self.peek()
            
            # Newlines
            if ch == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\\n', self.line, self.col))
                self.advance()
                continue
            
            # Comments (multiple styles)
            if ch == '#':
                while self.pos < len(self.source) and self.source[self.pos] != '\n':
                    self.advance()
                continue
            if ch == '/' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '/':
                while self.pos < len(self.source) and self.source[self.pos] != '\n':
                    self.advance()
                continue
            if self.source[self.pos:self.pos + 2] == '--':
                while self.pos < len(self.source) and self.source[self.pos] != '\n':
                    self.advance()
                continue
            
            # Numbers
            if ch.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if ch in ('"', "'"):
                self.tokens.append(self.read_string())
                continue
            
            # Parentheses
            if ch == '(':
                self.tokens.append(Token(TokenType.LPAREN, ch, self.line, self.col))
                self.advance()
                continue
            if ch == ')':
                self.tokens.append(Token(TokenType.RPAREN, ch, self.line, self.col))
                self.advance()
                continue
            
            # Braces
            if ch == '{':
                self.tokens.append(Token(TokenType.LBRACE, ch, self.line, self.col))
                self.advance()
                continue
            if ch == '}':
                self.tokens.append(Token(TokenType.RBRACE, ch, self.line, self.col))
                self.advance()
                continue
            
            # Brackets
            if ch == '[':
                self.tokens.append(Token(TokenType.LBRACKET, ch, self.line, self.col))
                self.advance()
                continue
            if ch == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ch, self.line, self.col))
                self.advance()
                continue
            
            # Comma
            if ch == ',':
                self.tokens.append(Token(TokenType.COMMA, ch, self.line, self.col))
                self.advance()
                continue
            
            # Semicolon (optional in EasyLang!)
            if ch == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ch, self.line, self.col))
                self.advance()
                continue
            
            # Operators (check for multi-char operators first!)
            if ch == '*' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '*':
                self.tokens.append(Token(TokenType.POWER, '**', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if ch == '=' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '=':
                self.tokens.append(Token(TokenType.EQUALS, '==', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if ch == '!' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '=':
                self.tokens.append(Token(TokenType.NOT_EQUALS, '!=', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if ch == '<' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if ch == '>' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if ch in '+-*/%=<>!':
                self.tokens.append(Token(self.OPERATORS.get(ch, TokenType.PLUS), ch, self.line, self.col))
                self.advance()
                continue
            
            # Identifiers and keywords
            if ch.isalpha() or ch == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # If we get here, it's an unexpected character
            self.error(f"Unexpected character: {repr(ch)} - I'm not sure what to do with this")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return self.tokens


class Parser:
    """
    Forgiving parser that:
    - Allows missing semicolons
    - Supports multiple syntax styles
    - Handles common mistakes gracefully
    - Provides helpful suggestions
    """
    
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0
        
    def error(self, msg: str):
        token = self.tokens[self.pos]
        # Friendly suggestions
        suggestions = {
            'SEMICOLON': "You can add a semicolon here, but it's optional!",
            'NEWLINE': "Try moving to the next line",
            'IDENTIFIER': "Did you mean to use a variable? Make sure it's defined!",
            'LPAREN': "You need an opening parenthesis here",
            'RPAREN': "You forgot a closing parenthesis!",
            'LBRACE': "You need an opening brace { here",
            'RBRACE': "You forgot a closing brace }!",
            'END': "Did you forget to close a block with 'end' or 'done'?",
        }
        
        friendly_msg = msg
        if token.type.name in suggestions:
            friendly_msg += f"\n  Hint: {suggestions[token.type.name]}"
        
        raise EasyLangError(friendly_msg, token.line, token.col)
    
    def peek(self) -> Token:
        return self.tokens[self.pos]
    
    def peek_ahead(self, n: int) -> Token:
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n]
        return Token(TokenType.EOF, None, 0, 0)
    
    def advance(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.peek()
        if token.type != token_type:
            self.error(f"Expected {token_type.name}, got {token.type.name}")
        return self.advance()
    
    def skip_newlines(self):
        while self.peek().type == TokenType.NEWLINE:
            self.advance()
    
    def optional_semicolon(self):
        """Semicolons are optional in EasyLang!"""
        if self.peek().type == TokenType.SEMICOLON:
            self.advance()
    
    def parse(self) -> list:
        """Parse program into AST"""
        statements = []
        
        self.skip_newlines()
        
        while self.peek().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return statements
    
    def parse_statement(self):
        """Parse a single statement - very forgiving!"""
        # Skip newlines (they're optional in EasyLang!)
        while self.peek().type == TokenType.NEWLINE:
            self.advance()
        
        token = self.peek()
        
        # Check for END token - this should not be parsed as a statement
        if token.type == TokenType.END:
            return None
        
        # Variable assignment (multiple syntaxes!)
        if token.type == TokenType.LET:
            return self.parse_assignment()
        
        # Handle "y is now 20" or "x gets 10" syntax
        if token.type == TokenType.IDENTIFIER:
            # Check if this is an assignment (e.g., "y is now 20")
            if (self.peek_ahead(1).type == TokenType.IDENTIFIER and 
                self.peek_ahead(1).value.lower() in ('is', 'now', 'gets', 'equal')):
                return self.parse_assignment()
            # Check if this is an assignment with EQUALS (e.g., "y equals 20")
            if self.peek_ahead(1).type == TokenType.EQUALS:
                return self.parse_assignment()
        
        # Print (multiple syntaxes!)
        if token.type == TokenType.PRINT:
            return self.parse_print()
        
        # Function definition (multiple syntaxes!)
        if token.type == TokenType.FUNCTION:
            return self.parse_func_def()
        
        # If statement (multiple syntaxes!)
        if token.type == TokenType.IF:
            return self.parse_if()
        
        # While loop (multiple syntaxes!)
        if token.type == TokenType.WHILE:
            return self.parse_while()
        
        # Repeat loop (multiple syntaxes!)
        if token.type == TokenType.REPEAT:
            return self.parse_repeat()
        
        # Return (multiple syntaxes!)
        if token.type == TokenType.RETURN:
            return self.parse_return()
        
        # Function call or expression
        return self.parse_expression_statement()
    
    def parse_assignment(self):
        """let variable = value (or many other forms!)"""
        token = self.peek()
        
        # Handle "y is now 20" syntax (no LET token)
        if token.type == TokenType.IDENTIFIER:
            name_token = self.advance()
            name = name_token.value
        else:
            # Consume 'let' (or synonym)
            self.advance()
            name_token = self.expect(TokenType.IDENTIFIER)
            name = name_token.value
        
        # Check for "is" or "be" or other assignment synonyms
        if (self.peek().type in (TokenType.IDENTIFIER, TokenType.EQUALS) and 
            (self.peek().value.lower() in ('is', 'be', 'now', 'gets', 'equals', 'equal') or
             self.peek().type == TokenType.EQUALS)):
            self.advance()
            # After consuming the synonym, check if next is ASSIGN
            if self.peek().type == TokenType.ASSIGN:
                self.advance()  # consume '='
            # Otherwise, the value follows directly (e.g., "make w equal 40")
            expr = self.parse_expression()
            self.optional_semicolon()
            return ('assign', name, expr, self.peek().line)
        
        # Handle "set x to y" - "to" is a keyword but we treat it as part of assignment
        if self.peek().type == TokenType.FUNCTION and self.peek().value.lower() == 'to':
            self.advance()  # consume 'to'
            # In this case, the value is the next expression (no = sign needed)
            expr = self.parse_expression()
            self.optional_semicolon()
            return ('assign', name, expr, self.peek().line)
        
        self.expect(TokenType.ASSIGN)
        expr = self.parse_expression()
        self.optional_semicolon()
        
        return ('assign', name, expr, self.peek().line)
    
    def parse_print(self):
        """print "message" (or many other forms!)"""
        self.advance()  # consume 'print' (or synonym)
        
        # Handle "print x" or "print the value of x" or "print x is: x"
        if self.peek().type == TokenType.IDENTIFIER and self.peek().value.lower() in ('the', 'the value of'):
            self.advance()
            if self.peek().type == TokenType.IDENTIFIER and self.peek().value.lower() == 'value':
                self.advance()
                if self.peek().type == TokenType.IDENTIFIER and self.peek().value.lower() == 'of':
                    self.advance()
        
        expr = self.parse_expression()
        self.optional_semicolon()
        
        return ('print', expr)
    
    def parse_func_def(self):
        """function name(params) { body } or to name(params) { body }"""
        self.advance()  # consume 'function' (or synonym)
        
        # Handle both "function greet(x)" and "to greet(x)" styles
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.LPAREN)
        
        params = []
        if self.peek().type != TokenType.RPAREN:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.peek().type == TokenType.COMMA:
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER).value)
        
        self.expect(TokenType.RPAREN)
        
        # Handle both { } and do/end styles
        if self.peek().type == TokenType.LBRACE:
            self.advance()
            body = []
            while self.peek().type != TokenType.RBRACE:
                body.append(self.parse_statement())
            self.expect(TokenType.RBRACE)
        else:
            # do/end style
            if self.peek().type in (TokenType.DO, TokenType.THEN):
                self.advance()
            body = []
            while self.peek().type not in (TokenType.END, TokenType.RBRACE):
                body.append(self.parse_statement())
            if self.peek().type == TokenType.END:
                self.advance()
        
        self.optional_semicolon()
        
        return ('func_def', name, params, body, self.peek().line)
    
    def parse_if(self):
        """if condition then body end (or many other forms!)"""
        self.advance()  # consume 'if' (or synonym)
        
        condition = self.parse_expression()
        
        # Handle multiple syntaxes
        if self.peek().type in (TokenType.THEN, TokenType.DO):
            self.advance()
        
        body = []
        while self.peek().type not in (TokenType.END, TokenType.ELSE, TokenType.RBRACE):
            body.append(self.parse_statement())
        
        else_body = None
        if self.peek().type == TokenType.ELSE:
            self.advance()
            else_body = []
            while self.peek().type not in (TokenType.END, TokenType.RBRACE):
                else_body.append(self.parse_statement())
        
        if self.peek().type == TokenType.END:
            self.advance()
        
        self.optional_semicolon()
        
        return ('if', condition, body, else_body, self.peek().line)
    
    def parse_while(self):
        """while condition do body end (or many other forms!)"""
        self.advance()  # consume 'while' (or synonym)
        
        condition = self.parse_expression()
        
        # Handle multiple syntaxes
        if self.peek().type in (TokenType.DO, TokenType.THEN):
            self.advance()
        
        body = []
        while self.peek().type not in (TokenType.END, TokenType.RBRACE):
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
        
        if self.peek().type == TokenType.END:
            self.advance()
        
        self.optional_semicolon()
        
        return ('while', condition, body, self.peek().line)
    
    def parse_repeat(self):
        """repeat N times body end (or many other forms!)"""
        self.advance()  # consume 'repeat' (or synonym)
        
        # Handle "repeat 10 times" or "loop 10x" or "do this 10 times"
        if self.peek().type == TokenType.IDENTIFIER and self.peek().value.lower() == 'this':
            self.advance()
        
        count = self.parse_expression()
        
        # Handle "times" or "iterations" or "rounds" or "x"
        if self.peek().type in (TokenType.TIMES, TokenType.IDENTIFIER):
            if self.peek().type == TokenType.TIMES:
                self.advance()
            elif self.peek().value.lower() in ('times', 'iterations', 'rounds', 'x'):
                self.advance()
        
        # Handle "do" or "then"
        if self.peek().type in (TokenType.DO, TokenType.THEN):
            self.advance()
        
        body = []
        while self.peek().type not in (TokenType.END, TokenType.RBRACE):
            body.append(self.parse_statement())
        
        if self.peek().type == TokenType.END:
            self.advance()
        
        self.optional_semicolon()
        
        return ('repeat', count, body, self.peek().line)
    
    def parse_return(self):
        """return expression (or give back expression)"""
        self.advance()  # consume 'return' (or synonym)
        
        # Handle "give back" or "send back"
        if self.peek().type == TokenType.IDENTIFIER and self.peek().value.lower() in ('back',):
            self.advance()
        
        expr = self.parse_expression()
        self.optional_semicolon()
        
        return ('return', expr, self.peek().line)
    
    def parse_expression_statement(self):
        """Expression followed by optional semicolon"""
        expr = self.parse_expression()
        self.optional_semicolon()
        return ('expr_stmt', expr)
    
    def parse_expression(self):
        return self.parse_or()
    
    def parse_or(self):
        left = self.parse_and()
        
        while self.peek().type == TokenType.OR:
            self.advance()
            right = self.parse_and()
            left = ('binop', 'or', left, right)
        
        return left
    
    def parse_and(self):
        left = self.parse_comparison()
        
        while self.peek().type == TokenType.AND:
            self.advance()
            right = self.parse_comparison()
            left = ('binop', 'and', left, right)
        
        return left
    
    def parse_comparison(self):
        left = self.parse_additive()
        
        while self.peek().type in (TokenType.EQUALS, TokenType.NOT_EQUALS, 
                                    TokenType.LESS, TokenType.GREATER,
                                    TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.advance()
            right = self.parse_additive()
            left = ('binop', op.value.lower() if isinstance(op.value, str) else op.type.name.lower(), left, right)
        
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance()
            right = self.parse_multiplicative()
            left = ('binop', op.value if isinstance(op.value, str) else op.type.name.lower(), left, right)
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_power()
        
        while self.peek().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance()
            right = self.parse_power()
            left = ('binop', op.value if isinstance(op.value, str) else op.type.name.lower(), left, right)
        
        return left
    
    def parse_power(self):
        left = self.parse_unary()
        
        if self.peek().type == TokenType.POWER:
            self.advance()
            right = self.parse_power()  # Right associative
            left = ('binop', 'power', left, right)
        
        return left
    
    def parse_unary(self):
        if self.peek().type == TokenType.MINUS:
            self.advance()
            expr = self.parse_unary()
            return ('unary', '-', expr)
        
        if self.peek().type == TokenType.NOT:
            self.advance()
            expr = self.parse_unary()
            return ('unary', 'not', expr)
        
        return self.parse_primary()
    
    def parse_primary(self):
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
        
        # Function call (check BEFORE identifier!)
        if token.type == TokenType.IDENTIFIER and self.peek_ahead(1).type == TokenType.LPAREN:
            name = self.advance().value
            self.expect(TokenType.LPAREN)
            args = []
            if self.peek().type != TokenType.RPAREN:
                args.append(self.parse_expression())
                while self.peek().type == TokenType.COMMA:
                    self.advance()
                    args.append(self.parse_expression())
            self.expect(TokenType.RPAREN)
            return ('func_call', name, args)
        
        # Identifier (variable)
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return ('var', token.value)
        
        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error(f"Unexpected token: {token.type.name} - did you mean to write something else?")


class Interpreter:
    """
    Interpreter that:
    - Handles type inference automatically
    - Provides friendly error messages
    - Supports natural language operators
    - Has smart defaults
    """
    
    def __init__(self):
        self.global_scope = {}
        self.functions = {}
        self.call_stack = []
        self.output = []
        
    def interpret(self, program: list):
        self.execute_block(program, self.global_scope)
        
    def execute_block(self, block: list, scope: dict):
        for stmt in block:
            self.execute_statement(stmt, scope)
    
    def execute_statement(self, stmt: tuple, scope: dict):
        if stmt[0] == 'assign':
            name, expr = stmt[1], stmt[2]
            value = self.evaluate(expr, scope)
            scope[name] = value
            
        elif stmt[0] == 'print':
            expr = stmt[1]
            value = self.evaluate(expr, scope)
            self.output.append(str(value))
            
        elif stmt[0] == 'func_def':
            name, params, body = stmt[1], stmt[2], stmt[3]
            self.functions[name] = (params, body)
            
        elif stmt[0] == 'if':
            condition, body, else_body = stmt[1], stmt[2], stmt[3]
            if self.evaluate(condition, scope):
                self.execute_block(body, scope.copy())
            elif else_body:
                self.execute_block(else_body, scope.copy())
                
        elif stmt[0] == 'while':
            condition, body = stmt[1], stmt[2]
            while self.evaluate(condition, scope):
                self.execute_block(body, scope)  # Don't copy scope - changes should persist
                
        elif stmt[0] == 'repeat':
            count, body = stmt[1], stmt[2]
            count_val = self.evaluate(count, scope)
            if isinstance(count_val, (int, float)):
                for _ in range(int(count_val)):
                    self.execute_block(body, scope.copy())
            else:
                raise EasyLangError(f"Repeat count must be a number, got {type(count_val).__name__}", 0, 0)
                
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
                # Friendly error with suggestion
                similar = [k for k in scope.keys() if k.lower().startswith(name.lower()[:3])]
                hint = f" Did you mean: {', '.join(similar)}?" if similar else ""
                raise EasyLangError(f"Variable '{name}' is not defined.{hint}", 0, 0)
        
        elif expr[0] == 'binop':
            op, left, right = expr[1], expr[2], expr[3]
            left_val = self.evaluate(left, scope)
            right_val = self.evaluate(right, scope)
            
            # Natural language operators
            if op in ('plus', '+'):
                return left_val + right_val
            elif op in ('minus', '-'):
                return left_val - right_val
            elif op in ('times', '*'):
                return left_val * right_val
            elif op in ('divided by', '/'):
                if right_val == 0:
                    raise EasyLangError("Cannot divide by zero!", 0, 0)
                return left_val / right_val
            elif op in ('modulo', '%'):
                return left_val % right_val
            elif op in ('power', '**'):
                return left_val ** right_val
            elif op in ('equals', '==', 'is'):
                return left_val == right_val
            elif op in ('not equal to', '!='):
                return left_val != right_val
            elif op in ('less than', '<'):
                return left_val < right_val
            elif op in ('greater than', '>'):
                return left_val > right_val
            elif op in ('less than or equal to', '<='):
                return left_val <= right_val
            elif op in ('greater than or equal to', '>='):
                return left_val >= right_val
            elif op == 'and':
                return left_val and right_val
            elif op == 'or':
                return left_val or right_val
        
        elif expr[0] == 'unary':
            op, operand = expr[1], expr[2]
            value = self.evaluate(operand, scope)
            if op == '-':
                return -value
            elif op == 'not':
                return not value
        
        elif expr[0] == 'func_call':
            name, args = expr[1], expr[2]
            
            if name not in self.functions:
                # Suggest similar functions
                similar = [k for k in self.functions.keys() if k.lower().startswith(name.lower()[:3])]
                hint = f" Did you mean: {', '.join(similar)}?" if similar else ""
                raise EasyLangError(f"Function '{name}' is not defined.{hint}", 0, 0)
            
            params, body = self.functions[name]
            arg_values = [self.evaluate(arg, scope) for arg in args]
            
            if len(params) != len(arg_values):
                raise EasyLangError(
                    f"Function {name} expects {len(params)} arguments, but you gave {len(arg_values)}.",
                    0, 0
                )
            
            func_scope = dict(zip(params, arg_values))
            
            try:
                self.execute_block(body, func_scope)
                return None
            except ReturnException as e:
                return e.value
        
        raise EasyLangError(f"Unknown expression type: {expr[0]}", 0, 0)


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


def run_easylang(source: str):
    """Main entry point for EasyLang interpreter"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    return interpreter.output


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 easylang.py <program.el>")
        print("\nExample program (save as hello.el):")
        print('''
# Hello World in EasyLang - pick any style you like!

print "Hello World!"

# Or use a different synonym:
say "Hello World!"

# Variables are easy too:
let x = 10
x is now 20
set y to 30

# Control flow is natural:
if x > 10 then
  print "x is big!"
end

# Loops are simple:
repeat 5 times
  print "Hello!"
end

# Functions are easy:
function greet(name)
  print "Hello, " + name + "!"
end

greet("World")
        ''')
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        output = run_easylang(source)
        
        for line in output:
            print(line)
            
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        sys.exit(1)
    except EasyLangError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
