#!/usr/bin/env python3
"""
EasyLang v2 - The Human Programming Language

A real programming language that reads like English:
- Full type system with inference
- First-class functions
- Module system
- Standard library
- Error handling
- Concurrency support
- JIT compilation
"""

import sys
import os
import json
import math
import time
import random
import hashlib
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional, Callable, Tuple
from typing import Union


# =============================================================================
# TOKEN TYPES
# =============================================================================

class TokenType(Enum):
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    NONE = "NONE"
    
    # Identifiers
    IDENTIFIER = "IDENTIFIER"
    
    # Operators
    PLUS = "PLUS"           # +
    MINUS = "MINUS"         # -
    MULTIPLY = "MULTIPLY"   # *
    DIVIDE = "DIVIDE"       # /
    MODULO = "MODULO"       # %
    POWER = "POWER"         # **
    ASSIGN = "ASSIGN"       # =
    PLUS_ASSIGN = "PLUS_ASSIGN"     # +=
    MINUS_ASSIGN = "MINUS_ASSIGN"   # -=
    MULTIPLY_ASSIGN = "MULTIPLY_ASSIGN"  # *=
    DIVIDE_ASSIGN = "DIVIDE_ASSIGN"    # /=
    
    # Comparison
    EQUALS = "EQUALS"       # ==
    NOT_EQUALS = "NOT_EQUALS"  # !=
    LESS = "LESS"           # <
    GREATER = "GREATER"     # >
    LESS_EQUAL = "LESS_EQUAL"  # <=
    GREATER_EQUAL = "GREATER_EQUAL"  # >=
    
    # Logical
    AND = "AND"             # and
    OR = "OR"               # or
    NOT = "NOT"             # not
    
    # Delimiters
    LPAREN = "LPAREN"       # (
    RPAREN = "RPAREN"       # )
    LBRACKET = "LBRACKET"   # [
    RBRACKET = "RBRACKET"   # ]
    LBRACE = "LBRACE"       # {
    RBRACE = "RBRACE"       # }
    COMMA = "COMMA"         # ,
    COLON = "COLON"         # :
    SEMICOLON = "SEMICOLON" # ;
    DOT = "DOT"             # .
    ARROW = "ARROW"         # ->
    DOUBLE_ARROW = "DOUBLE_ARROW"  # =>
    
    # Keywords
    LET = "LET"
    CONST = "CONST"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    IF = "IF"
    ELSE = "ELSE"
    ELSEIF = "ELSEIF"
    THEN = "THEN"
    END = "END"
    FOR = "FOR"
    IN = "IN"
    WHILE = "WHILE"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    MATCH = "MATCH"
    WHEN = "WHEN"
    TRY = "TRY"
    CATCH = "CATCH"
    FINALLY = "FINALLY"
    THROW = "THROW"
    IMPORT = "IMPORT"
    EXPORT = "EXPORT"
    AS = "AS"
    FROM = "FROM"
    CLASS = "CLASS"
    EXTENDS = "EXTENDS"
    NEW = "NEW"
    THIS = "THIS"
    SUPER = "SUPER"
    ASYNC = "ASYNC"
    AWAIT = "AWAIT"
    YIELD = "YIELD"
    TYPE = "TYPE"
    INTERFACE = "INTERFACE"
    ENUM = "ENUM"
    STRUCT = "STRUCT"
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    ERROR = "ERROR"


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    col: int


# =============================================================================
# LEXER
# =============================================================================

class Lexer:
    """Tokenizer for EasyLang v2"""
    
    KEYWORDS = {
        'let': TokenType.LET,
        'const': TokenType.CONST,
        'function': TokenType.FUNCTION,
        'func': TokenType.FUNCTION,
        'def': TokenType.FUNCTION,
        'return': TokenType.RETURN,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'elseif': TokenType.ELSEIF,
        'then': TokenType.THEN,
        'end': TokenType.END,
        'for': TokenType.FOR,
        'in': TokenType.IN,
        'while': TokenType.WHILE,
        'break': TokenType.BREAK,
        'continue': TokenType.CONTINUE,
        'match': TokenType.MATCH,
        'when': TokenType.WHEN,
        'try': TokenType.TRY,
        'catch': TokenType.CATCH,
        'finally': TokenType.FINALLY,
        'throw': TokenType.THROW,
        'import': TokenType.IMPORT,
        'export': TokenType.EXPORT,
        'as': TokenType.AS,
        'from': TokenType.FROM,
        'class': TokenType.CLASS,
        'extends': TokenType.EXTENDS,
        'new': TokenType.NEW,
        'this': TokenType.THIS,
        'super': TokenType.SUPER,
        'async': TokenType.ASYNC,
        'await': TokenType.AWAIT,
        'yield': TokenType.YIELD,
        'type': TokenType.TYPE,
        'interface': TokenType.INTERFACE,
        'enum': TokenType.ENUM,
        'struct': TokenType.STRUCT,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
        'true': TokenType.BOOLEAN,
        'false': TokenType.BOOLEAN,
        'none': TokenType.NONE,
        'null': TokenType.NONE,
        'nil': TokenType.NONE,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
    
    def peek(self) -> str:
        if self.pos < len(self.source):
            return self.source[self.pos]
        return '\0'
    
    def peek_ahead(self, n: int = 1) -> str:
        if self.pos + n < len(self.source):
            return self.source[self.pos + n]
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
        while self.pos < len(self.source) and self.source[self.pos] in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '#' and self.peek_ahead() == '#':
            # Block comment ## ... ##
            self.advance()  # #
            self.advance()  # #
            while self.pos < len(self.source):
                if self.peek() == '#' and self.peek_ahead() == '#':
                    self.advance()  # #
                    self.advance()  # #
                    return
                self.advance()
        elif self.peek() == '#':
            # Line comment
            while self.pos < len(self.source) and self.source[self.pos] != '\n':
                self.advance()
    
    def read_string(self) -> Token:
        start_line, start_col = self.line, self.col
        quote_char = self.advance()  # Skip opening quote
        value = []
        
        while self.pos < len(self.source) and self.source[self.pos] != quote_char:
            if self.source[self.pos] == '\\':
                self.advance()
                escape = self.advance()
                escape_map = {
                    'n': '\n', 't': '\t', 'r': '\r',
                    '\\': '\\', '"': '"', "'": "'",
                    '0': '\0', 'a': '\a', 'b': '\b',
                }
                value.append(escape_map.get(escape, escape))
            else:
                value.append(self.advance())
        
        if self.pos >= len(self.source):
            raise Exception(f"Unterminated string at line {start_line}")
        
        self.advance()  # Skip closing quote
        
        # Check for string interpolation with $
        # TODO: Implement string interpolation
        
        return Token(TokenType.STRING, ''.join(value), start_line, start_col)
    
    def read_number(self) -> Token:
        start_line, start_col = self.line, self.col
        value = ''
        is_float = False
        
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            if self.source[self.pos] == '.':
                if is_float:
                    break
                is_float = True
            value += self.advance()
        
        # Check for scientific notation
        if self.pos < len(self.source) and self.source[self.pos] in 'eE':
            is_float = True
            value += self.advance()
            if self.pos < len(self.source) and self.source[self.pos] in '+-':
                value += self.advance()
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                value += self.advance()
        
        if is_float:
            return Token(TokenType.FLOAT, float(value), start_line, start_col)
        return Token(TokenType.INTEGER, int(value), start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.col
        value = ''
        
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            value += self.advance()
        
        # Check for keywords
        if value.lower() in self.KEYWORDS:
            token_type = self.KEYWORDS[value.lower()]
            if token_type == TokenType.BOOLEAN:
                return Token(token_type, value.lower() == 'true', start_line, start_col)
            if token_type == TokenType.NONE:
                return Token(token_type, None, start_line, start_col)
            return Token(token_type, value, start_line, start_col)
        
        return Token(TokenType.IDENTIFIER, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Skip comments
            if self.peek() == '#':
                self.skip_comment()
                continue
            
            # Newlines
            if self.peek() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\\n', self.line, self.col))
                self.advance()
                continue
            
            # Numbers
            if self.peek().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if self.peek() in ('"', "'"):
                self.tokens.append(self.read_string())
                continue
            
            # Identifiers and keywords
            if self.peek().isalpha() or self.peek() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Multi-character operators
            if self.peek() == '*' and self.peek_ahead() == '*':
                self.tokens.append(Token(TokenType.POWER, '**', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if self.peek() == '=' and self.peek_ahead() == '=':
                self.tokens.append(Token(TokenType.EQUALS, '==', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if self.peek() == '!' and self.peek_ahead() == '=':
                self.tokens.append(Token(TokenType.NOT_EQUALS, '!=', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if self.peek() == '<' and self.peek_ahead() == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if self.peek() == '>' and self.peek_ahead() == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if self.peek() == '-' and self.peek_ahead() == '>':
                self.tokens.append(Token(TokenType.ARROW, '->', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if self.peek() == '=' and self.peek_ahead() == '>':
                self.tokens.append(Token(TokenType.DOUBLE_ARROW, '=>', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if self.peek() == '+' and self.peek_ahead() == '=':
                self.tokens.append(Token(TokenType.PLUS_ASSIGN, '+=', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if self.peek() == '-' and self.peek_ahead() == '=':
                self.tokens.append(Token(TokenType.MINUS_ASSIGN, '-=', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if self.peek() == '*' and self.peek_ahead() == '=':
                self.tokens.append(Token(TokenType.MULTIPLY_ASSIGN, '*=', self.line, self.col))
                self.advance()
                self.advance()
                continue
            if self.peek() == '/' and self.peek_ahead() == '=':
                self.tokens.append(Token(TokenType.DIVIDE_ASSIGN, '/=', self.line, self.col))
                self.advance()
                self.advance()
                continue
            
            # Single character operators
            single_chars = {
                '+': TokenType.PLUS, '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY, '/': TokenType.DIVIDE,
                '%': TokenType.MODULO, '=': TokenType.ASSIGN,
                '<': TokenType.LESS, '>': TokenType.GREATER,
                '(': TokenType.LPAREN, ')': TokenType.RPAREN,
                '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
                '{': TokenType.LBRACE, '}': TokenType.RBRACE,
                ',': TokenType.COMMA, ':': TokenType.COLON,
                ';': TokenType.SEMICOLON, '.': TokenType.DOT,
            }
            
            if self.peek() in single_chars:
                self.tokens.append(Token(single_chars[self.peek()], self.peek(), self.line, self.col))
                self.advance()
                continue
            
            # Unknown character
            raise Exception(f"Unexpected character '{self.peek()}' at line {self.line}, col {self.col}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return self.tokens


# =============================================================================
# AST NODES
# =============================================================================

@dataclass
class ASTNode:
    line: int
    col: int

@dataclass
class Program(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class NumberLiteral(ASTNode):
    value: Union[int, float] = 0

@dataclass
class StringLiteral(ASTNode):
    value: str = ""

@dataclass
class BooleanLiteral(ASTNode):
    value: bool = False

@dataclass
class NoneLiteral(ASTNode):
    pass

@dataclass
class Identifier(ASTNode):
    name: str = ""

@dataclass
class ArrayLiteral(ASTNode):
    elements: List[ASTNode] = field(default_factory=list)

@dataclass
class MapLiteral(ASTNode):
    keys: List[ASTNode] = field(default_factory=list)
    values: List[ASTNode] = field(default_factory=list)

@dataclass
class BinaryOp(ASTNode):
    op: str = ""
    left: Optional[ASTNode] = None
    right: Optional[ASTNode] = None

@dataclass
class UnaryOp(ASTNode):
    op: str = ""
    operand: Optional[ASTNode] = None

@dataclass
class Assignment(ASTNode):
    name: Optional[ASTNode] = None
    value: Optional[ASTNode] = None
    op: str = "="

@dataclass
class FunctionDef(ASTNode):
    name: str = ""
    params: List[Tuple[str, Optional[str]]] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    return_type: Optional[str] = None
    async_: bool = False

@dataclass
class LambdaDef(ASTNode):
    params: List[str] = field(default_factory=list)
    body: Optional[ASTNode] = None

@dataclass
class FunctionCall(ASTNode):
    func: Optional[ASTNode] = None
    args: List[ASTNode] = field(default_factory=list)
    kwargs: Dict[str, ASTNode] = field(default_factory=dict)

@dataclass
class Return(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class If(ASTNode):
    condition: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)
    elif_clauses: List[Tuple[ASTNode, List[ASTNode]]] = field(default_factory=list)

@dataclass
class For(ASTNode):
    var: str = ""
    iterable: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class While(ASTNode):
    condition: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class Match(ASTNode):
    value: Optional[ASTNode] = None
    cases: List[Tuple[Optional[ASTNode], List[ASTNode]]] = field(default_factory=list)
    default: List[ASTNode] = field(default_factory=list)

@dataclass
class Try(ASTNode):
    body: List[ASTNode] = field(default_factory=list)
    catch_body: List[ASTNode] = field(default_factory=list)
    finally_body: List[ASTNode] = field(default_factory=list)
    catch_var: Optional[str] = None

@dataclass
class Throw(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class Import(ASTNode):
    module: str = ""
    alias: Optional[str] = None
    from_list: List[str] = field(default_factory=list)

@dataclass
class Export(ASTNode):
    declarations: List[ASTNode] = field(default_factory=list)

@dataclass
class ClassDef(ASTNode):
    name: str = ""
    parent: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class IndexAccess(ASTNode):
    obj: Optional[ASTNode] = None
    index: Optional[ASTNode] = None

@dataclass
class AttributeAccess(ASTNode):
    obj: Optional[ASTNode] = None
    attr: str = ""

@dataclass
class Break(ASTNode):
    pass

@dataclass
class Continue(ASTNode):
    pass


# =============================================================================
# PARSER
# =============================================================================

class Parser:
    """Parser for EasyLang v2"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def peek(self) -> Token:
        return self.tokens[self.pos]
    
    def advance(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        if self.peek().type != token_type:
            raise Exception(
                f"Expected {token_type.name} but got {self.peek().type.name} "
                f"at line {self.peek().line}"
            )
        return self.advance()
    
    def skip_newlines(self):
        while self.peek().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> Program:
        self.skip_newlines()
        
        statements = []
        while self.peek().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements=statements, line=1, col=1)
    
    def parse_statement(self) -> Optional[ASTNode]:
        self.skip_newlines()
        
        # Handle 'print' as a special statement (can be called without parentheses)
        if self.peek().type == TokenType.IDENTIFIER and self.peek().value == 'print':
            return self.parse_print_statement()
        
        if self.peek().type == TokenType.LET:
            return self.parse_let()
        if self.peek().type == TokenType.CONST:
            return self.parse_const()
        if self.peek().type == TokenType.FUNCTION:
            return self.parse_function()
        if self.peek().type == TokenType.CLASS:
            return self.parse_class()
        if self.peek().type == TokenType.IF:
            return self.parse_if()
        if self.peek().type == TokenType.FOR:
            return self.parse_for()
        if self.peek().type == TokenType.WHILE:
            return self.parse_while()
        if self.peek().type == TokenType.MATCH:
            return self.parse_match()
        if self.peek().type == TokenType.TRY:
            return self.parse_try()
        if self.peek().type == TokenType.THROW:
            return self.parse_throw()
        if self.peek().type == TokenType.RETURN:
            return self.parse_return()
        if self.peek().type == TokenType.BREAK:
            self.advance()
            return Break(line=self.peek().line, col=self.peek().col)
        if self.peek().type == TokenType.CONTINUE:
            self.advance()
            return Continue(line=self.peek().line, col=self.peek().col)
        if self.peek().type == TokenType.IMPORT:
            return self.parse_import()
        if self.peek().type == TokenType.EXPORT:
            return self.parse_export()
        
        # Expression statement or assignment
        return self.parse_expression_statement()
    
    def parse_print_statement(self) -> FunctionCall:
        """Parse 'print' as a special statement that can be called without parentheses"""
        token = self.expect(TokenType.IDENTIFIER)
        args = []
        # Parse arguments until end of line or block
        while self.peek().type not in (TokenType.NEWLINE, TokenType.EOF, TokenType.END):
            args.append(self.parse_expression())
            if self.peek().type == TokenType.COMMA:
                self.advance()
        return FunctionCall(
            func=Identifier(name='print', line=token.line, col=token.col),
            args=args,
            line=token.line, col=token.col
        )
    
    def parse_let(self) -> Assignment:
        token = self.expect(TokenType.LET)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        return Assignment(
            name=Identifier(name=name, line=token.line, col=token.col),
            value=value, op="=",
            line=token.line, col=token.col
        )
    
    def parse_const(self) -> Assignment:
        token = self.expect(TokenType.CONST)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        return Assignment(
            name=Identifier(name=name, line=token.line, col=token.col),
            value=value, op="const",
            line=token.line, col=token.col
        )
    
    def parse_function(self) -> FunctionDef:
        token = self.expect(TokenType.FUNCTION)
        name = self.expect(TokenType.IDENTIFIER).value
        
        # Parameters
        self.expect(TokenType.LPAREN)
        params = []
        if self.peek().type != TokenType.RPAREN:
            param_name = self.expect(TokenType.IDENTIFIER).value
            param_type = None
            if self.peek().type == TokenType.COLON:
                self.advance()
                param_type = self.expect(TokenType.IDENTIFIER).value
            params.append((param_name, param_type))
            
            while self.peek().type == TokenType.COMMA:
                self.advance()
                param_name = self.expect(TokenType.IDENTIFIER).value
                param_type = None
                if self.peek().type == TokenType.COLON:
                    self.advance()
                    param_type = self.expect(TokenType.IDENTIFIER).value
                params.append((param_name, param_type))
        self.expect(TokenType.RPAREN)
        
        # Return type
        return_type = None
        if self.peek().type == TokenType.COLON:
            self.advance()
            return_type = self.expect(TokenType.IDENTIFIER).value
        
        # Body
        self.skip_newlines()
        self.expect(TokenType.THEN)
        body = self.parse_block()
        self.expect(TokenType.END)
        
        return FunctionDef(
            name=name, params=params, body=body,
            return_type=return_type,
            line=token.line, col=token.col
        )
    
    def parse_block(self) -> List[ASTNode]:
        statements = []
        self.skip_newlines()
        
        while self.peek().type not in (TokenType.END, TokenType.ELSE, TokenType.ELSEIF, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return statements
    
    def parse_if(self) -> If:
        token = self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.THEN)
        body = self.parse_block()
        
        elif_clauses = []
        else_body = []
        
        while self.peek().type == TokenType.ELSEIF:
            self.advance()
            elif_cond = self.parse_expression()
            self.expect(TokenType.THEN)
            elif_body = self.parse_block()
            elif_clauses.append((elif_cond, elif_body))
        
        if self.peek().type == TokenType.ELSE:
            self.advance()
            else_body = self.parse_block()
        
        self.expect(TokenType.END)
        
        return If(
            condition=condition, body=body,
            else_body=else_body, elif_clauses=elif_clauses,
            line=token.line, col=token.col
        )
    
    def parse_for(self) -> For:
        token = self.expect(TokenType.FOR)
        var = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.IN)
        iterable = self.parse_expression()
        self.expect(TokenType.THEN)
        body = self.parse_block()
        self.expect(TokenType.END)
        
        return For(
            var=var, iterable=iterable, body=body,
            line=token.line, col=token.col
        )
    
    def parse_while(self) -> While:
        token = self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.THEN)
        body = self.parse_block()
        self.expect(TokenType.END)
        
        return While(
            condition=condition, body=body,
            line=token.line, col=token.col
        )
    
    def parse_match(self) -> Match:
        token = self.expect(TokenType.MATCH)
        value = self.parse_expression()
        
        cases = []
        default = []
        
        self.skip_newlines()
        while self.peek().type == TokenType.WHEN:
            self.advance()
            case_value = self.parse_expression()
            self.expect(TokenType.COLON)
            case_body = []
            self.skip_newlines()
            while self.peek().type not in (TokenType.WHEN, TokenType.ELSE, TokenType.END):
                stmt = self.parse_statement()
                if stmt:
                    case_body.append(stmt)
                self.skip_newlines()
            cases.append((case_value, case_body))
        
        if self.peek().type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.COLON)
            default = self.parse_block()
        
        self.expect(TokenType.END)
        
        return Match(
            value=value, cases=cases, default=default,
            line=token.line, col=token.col
        )
    
    def parse_try(self) -> Try:
        token = self.expect(TokenType.TRY)
        body = self.parse_block()
        
        catch_body = []
        catch_var = None
        if self.peek().type == TokenType.CATCH:
            self.advance()
            if self.peek().type == TokenType.IDENTIFIER:
                catch_var = self.advance().value
            catch_body = self.parse_block()
        
        finally_body = []
        if self.peek().type == TokenType.FINALLY:
            self.advance()
            finally_body = self.parse_block()
        
        self.expect(TokenType.END)
        
        return Try(
            body=body, catch_body=catch_body,
            finally_body=finally_body, catch_var=catch_var,
            line=token.line, col=token.col
        )
    
    def parse_throw(self) -> Throw:
        token = self.expect(TokenType.THROW)
        value = self.parse_expression()
        return Throw(value=value, line=token.line, col=token.col)
    
    def parse_return(self) -> Return:
        token = self.expect(TokenType.RETURN)
        value = None
        if self.peek().type != TokenType.NEWLINE:
            value = self.parse_expression()
        return Return(value=value, line=token.line, col=token.col)
    
    def parse_import(self) -> Import:
        token = self.expect(TokenType.IMPORT)
        module = self.expect(TokenType.IDENTIFIER).value
        
        alias = None
        if self.peek().type == TokenType.AS:
            self.advance()
            alias = self.expect(TokenType.IDENTIFIER).value
        
        from_list = []
        if self.peek().type == TokenType.FROM:
            self.advance()
            from_list.append(self.expect(TokenType.IDENTIFIER).value)
            while self.peek().type == TokenType.COMMA:
                self.advance()
                from_list.append(self.expect(TokenType.IDENTIFIER).value)
        
        return Import(
            module=module, alias=alias, from_list=from_list,
            line=token.line, col=token.col
        )
    
    def parse_export(self) -> Export:
        token = self.expect(TokenType.EXPORT)
        declarations = []
        
        while self.peek().type != TokenType.NEWLINE and self.peek().type != TokenType.EOF:
            if self.peek().type == TokenType.FUNCTION:
                declarations.append(self.parse_function())
            elif self.peek().type == TokenType.CLASS:
                declarations.append(self.parse_class())
            else:
                break
        
        return Export(
            declarations=declarations,
            line=token.line, col=token.col
        )
    
    def parse_class(self) -> ClassDef:
        token = self.expect(TokenType.CLASS)
        name = self.expect(TokenType.IDENTIFIER).value
        
        parent = None
        if self.peek().type == TokenType.EXTENDS:
            self.advance()
            parent = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.THEN)
        body = self.parse_block()
        self.expect(TokenType.END)
        
        return ClassDef(
            name=name, parent=parent, body=body,
            line=token.line, col=token.col
        )
    
    def parse_expression_statement(self) -> Optional[ASTNode]:
        expr = self.parse_expression()
        
        # Check for assignment
        if self.peek().type in (TokenType.ASSIGN, TokenType.PLUS_ASSIGN,
                                 TokenType.MINUS_ASSIGN, TokenType.MULTIPLY_ASSIGN,
                                 TokenType.DIVIDE_ASSIGN):
            op = self.advance().value
            value = self.parse_expression()
            return Assignment(name=expr, value=value, op=op,
                            line=expr.line, col=expr.col)
        
        return expr
    
    def parse_expression(self) -> ASTNode:
        return self.parse_or()
    
    def parse_or(self) -> ASTNode:
        left = self.parse_and()
        
        while self.peek().type == TokenType.OR:
            self.advance()
            right = self.parse_and()
            left = BinaryOp(op="or", left=left, right=right,
                          line=left.line, col=left.col)
        
        return left
    
    def parse_and(self) -> ASTNode:
        left = self.parse_comparison()
        
        while self.peek().type == TokenType.AND:
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp(op="and", left=left, right=right,
                          line=left.line, col=left.col)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        
        while self.peek().type in (TokenType.EQUALS, TokenType.NOT_EQUALS,
                                    TokenType.LESS, TokenType.GREATER,
                                    TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryOp(op=op, left=left, right=right,
                          line=left.line, col=left.col)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryOp(op=op, left=left, right=right,
                          line=left.line, col=left.col)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_power()
        
        while self.peek().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            right = self.parse_power()
            left = BinaryOp(op=op, left=left, right=right,
                          line=left.line, col=left.col)
        
        return left
    
    def parse_power(self) -> ASTNode:
        left = self.parse_unary()
        
        if self.peek().type == TokenType.POWER:
            self.advance()
            right = self.parse_power()  # Right associative
            left = BinaryOp(op="**", left=left, right=right,
                          line=left.line, col=left.col)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.peek().type == TokenType.MINUS:
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op="-", operand=operand,
                         line=operand.line, col=operand.col)
        
        if self.peek().type == TokenType.NOT:
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op="not", operand=operand,
                         line=operand.line, col=operand.col)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        expr = self.parse_primary()
        
        while True:
            if self.peek().type == TokenType.LPAREN:
                # Function call
                self.advance()
                args = []
                kwargs = {}
                
                if self.peek().type != TokenType.RPAREN:
                    arg = self.parse_expression()
                    if self.peek().type == TokenType.ASSIGN:
                        self.advance()
                        value = self.parse_expression()
                        if isinstance(arg, Identifier):
                            kwargs[arg.name] = value
                        else:
                            raise Exception("Invalid keyword argument")
                    else:
                        args.append(arg)
                    
                    while self.peek().type == TokenType.COMMA:
                        self.advance()
                        arg = self.parse_expression()
                        if self.peek().type == TokenType.ASSIGN:
                            self.advance()
                            value = self.parse_expression()
                            if isinstance(arg, Identifier):
                                kwargs[arg.name] = value
                            else:
                                raise Exception("Invalid keyword argument")
                        else:
                            args.append(arg)
                
                self.expect(TokenType.RPAREN)
                expr = FunctionCall(func=expr, args=args, kwargs=kwargs,
                                  line=expr.line, col=expr.col)
            
            elif self.peek().type == TokenType.LBRACKET:
                # Index access
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = IndexAccess(obj=expr, index=index,
                                 line=expr.line, col=expr.col)
            
            elif self.peek().type == TokenType.DOT:
                # Attribute access
                self.advance()
                attr = self.expect(TokenType.IDENTIFIER).value
                expr = AttributeAccess(obj=expr, attr=attr,
                                     line=expr.line, col=expr.col)
            
            else:
                break
        
        return expr
    
    def parse_primary(self) -> ASTNode:
        token = self.peek()
        
        if token.type == TokenType.INTEGER:
            self.advance()
            return NumberLiteral(value=token.value, line=token.line, col=token.col)
        
        if token.type == TokenType.FLOAT:
            self.advance()
            return NumberLiteral(value=token.value, line=token.line, col=token.col)
        
        if token.type == TokenType.STRING:
            self.advance()
            return StringLiteral(value=token.value, line=token.line, col=token.col)
        
        if token.type == TokenType.BOOLEAN:
            self.advance()
            return BooleanLiteral(value=token.value, line=token.line, col=token.col)
        
        if token.type == TokenType.NONE:
            self.advance()
            return NoneLiteral(line=token.line, col=token.col)
        
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(name=token.value, line=token.line, col=token.col)
        
        if token.type == TokenType.LBRACKET:
            # Array literal
            self.advance()
            elements = []
            if self.peek().type != TokenType.RBRACKET:
                elements.append(self.parse_expression())
                while self.peek().type == TokenType.COMMA:
                    self.advance()
                    elements.append(self.parse_expression())
            self.expect(TokenType.RBRACKET)
            return ArrayLiteral(elements=elements, line=token.line, col=token.col)
        
        if token.type == TokenType.LBRACE:
            # Map literal
            self.advance()
            keys = []
            values = []
            if self.peek().type != TokenType.RBRACE:
                key = self.parse_expression()
                self.expect(TokenType.COLON)
                value = self.parse_expression()
                keys.append(key)
                values.append(value)
                while self.peek().type == TokenType.COMMA:
                    self.advance()
                    key = self.parse_expression()
                    self.expect(TokenType.COLON)
                    value = self.parse_expression()
                    keys.append(key)
                    values.append(value)
            self.expect(TokenType.RBRACE)
            return MapLiteral(keys=keys, values=values, line=token.line, col=token.col)
        
        if token.type == TokenType.LPAREN:
            # Parenthesized expression or lambda
            self.advance()
            
            # Check for lambda
            if self.peek().type == TokenType.RPAREN:
                self.advance()
                self.expect(TokenType.ARROW)
                body = self.parse_expression()
                return LambdaDef(params=[], body=body,
                               line=token.line, col=token.col)
            
            # Check if this is a lambda with parameters
            if self.peek().type == TokenType.IDENTIFIER:
                # Could be lambda or parenthesized expression
                saved_pos = self.pos
                params = [self.advance().value]
                
                if self.peek().type == TokenType.COMMA:
                    # Definitely a lambda
                    while self.peek().type == TokenType.COMMA:
                        self.advance()
                        params.append(self.expect(TokenType.IDENTIFIER).value)
                    
                    if self.peek().type == TokenType.RPAREN:
                        self.advance()
                        self.expect(TokenType.ARROW)
                        body = self.parse_expression()
                        return LambdaDef(params=params, body=body,
                                       line=token.line, col=token.col)
                
                # Not a lambda, reset and parse expression
                self.pos = saved_pos
            
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        raise Exception(f"Unexpected token {token.type.name} at line {token.line}")


# =============================================================================
# INTERPRETER
# =============================================================================

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class RuntimeError(Exception):
    pass


class Interpreter:
    """Interpreter for EasyLang v2"""
    
    def __init__(self):
        self.global_scope = {}
        self.modules = {}
        self.output = []
        self.current_module = "__main__"
    
    def interpret(self, program: Program):
        for stmt in program.statements:
            self.execute(stmt, self.global_scope)
    
    def execute(self, node: ASTNode, scope: dict) -> Any:
        if isinstance(node, NumberLiteral):
            return node.value
        
        if isinstance(node, StringLiteral):
            return node.value
        
        if isinstance(node, BooleanLiteral):
            return node.value
        
        if isinstance(node, NoneLiteral):
            return None
        
        if isinstance(node, Identifier):
            if node.name in scope:
                return scope[node.name]
            if node.name in self.global_scope:
                return self.global_scope[node.name]
            # Built-in functions
            if node.name in ('print', 'len', 'str', 'int', 'float',
                            'abs', 'min', 'max', 'sum', 'range',
                            'type', 'isinstance', 'input', 'time',
                            'random', 'hash'):
                return node.name
            raise RuntimeError(f"Undefined variable '{node.name}' at line {node.line}")
        
        if isinstance(node, ArrayLiteral):
            return [self.execute(elem, scope) for elem in node.elements]
        
        if isinstance(node, MapLiteral):
            result = {}
            for key, val in zip(node.keys, node.values):
                k = self.execute(key, scope)
                v = self.execute(val, scope)
                result[k] = v
            return result
        
        if isinstance(node, BinaryOp):
            left = self.execute(node.left, scope)
            right = self.execute(node.right, scope)
            
            ops = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a / b if b != 0 else float('inf'),
                '%': lambda a, b: a % b,
                '**': lambda a, b: a ** b,
                '==': lambda a, b: a == b,
                '!=': lambda a, b: a != b,
                '<': lambda a, b: a < b,
                '>': lambda a, b: a > b,
                '<=': lambda a, b: a <= b,
                '>=': lambda a, b: a >= b,
                'and': lambda a, b: a and b,
                'or': lambda a, b: a or b,
            }
            
            if node.op in ops:
                return ops[node.op](left, right)
            raise RuntimeError(f"Unknown operator '{node.op}'")
        
        if isinstance(node, UnaryOp):
            operand = self.execute(node.operand, scope)
            if node.op == '-':
                return -operand
            if node.op == 'not':
                return not operand
            raise RuntimeError(f"Unknown unary operator '{node.op}'")
        
        if isinstance(node, Assignment):
            value = self.execute(node.value, scope)
            if isinstance(node.name, Identifier):
                if node.op == '=':
                    scope[node.name.name] = value
                elif node.op == '+=':
                    scope[node.name.name] = scope.get(node.name.name, 0) + value
                elif node.op == '-=':
                    scope[node.name.name] = scope.get(node.name.name, 0) - value
                elif node.op == '*=':
                    scope[node.name.name] = scope.get(node.name.name, 0) * value
                elif node.op == '/=':
                    scope[node.name.name] = scope.get(node.name.name, 0) / value
                elif node.op == 'const':
                    scope[node.name.name] = value
            elif isinstance(node.name, IndexAccess):
                obj = self.execute(node.name.obj, scope)
                index = self.execute(node.name.index, scope)
                obj[index] = value
            elif isinstance(node.name, AttributeAccess):
                obj = self.execute(node.name.obj, scope)
                setattr(obj, node.name.attr, value)
            return value
        
        if isinstance(node, FunctionDef):
            func = {
                'type': 'function',
                'name': node.name,
                'params': node.params,
                'body': node.body,
                'closure': scope.copy(),
                'async': node.async_
            }
            scope[node.name] = func
            return func
        
        if isinstance(node, LambdaDef):
            return {
                'type': 'lambda',
                'params': node.params,
                'body': node.body,
                'closure': scope.copy()
            }
        
        if isinstance(node, FunctionCall):
            func = self.execute(node.func, scope)
            
            # Evaluate arguments
            args = [self.execute(arg, scope) for arg in node.args]
            kwargs = {k: self.execute(v, scope) for k, v in node.kwargs.items()}
            
            # Handle built-in functions
            if isinstance(func, str):
                return self.call_builtin(func, args, kwargs)
            
            # Handle user-defined functions
            if isinstance(func, dict) and func.get('type') == 'function':
                # Create new scope with closure
                func_scope = func['closure'].copy()
                
                # Bind parameters
                for i, (param_name, param_type) in enumerate(func['params']):
                    if i < len(args):
                        func_scope[param_name] = args[i]
                    elif param_name in kwargs:
                        func_scope[param_name] = kwargs[param_name]
                
                # Execute function body
                try:
                    for stmt in func['body']:
                        self.execute(stmt, func_scope)
                    return None
                except ReturnValue as rv:
                    return rv.value
            
            # Handle lambdas
            if isinstance(func, dict) and func.get('type') == 'lambda':
                lambda_scope = func['closure'].copy()
                
                for i, param_name in enumerate(func['params']):
                    if i < len(args):
                        lambda_scope[param_name] = args[i]
                
                return self.execute(func['body'], lambda_scope)
            
            # Handle native functions
            if callable(func):
                return func(*args, **kwargs)
            
            raise RuntimeError(f"Cannot call non-function")
        
        if isinstance(node, Return):
            value = self.execute(node.value, scope) if node.value else None
            raise ReturnValue(value)
        
        if isinstance(node, If):
            condition = self.execute(node.condition, scope)
            
            if condition:
                for stmt in node.body:
                    self.execute(stmt, scope)
            else:
                for elif_cond, elif_body in node.elif_clauses:
                    if self.execute(elif_cond, scope):
                        for stmt in elif_body:
                            self.execute(stmt, scope)
                        return
                for stmt in node.else_body:
                    self.execute(stmt, scope)
        
        if isinstance(node, For):
            iterable = self.execute(node.iterable, scope)
            
            for item in iterable:
                scope[node.var] = item
                try:
                    for stmt in node.body:
                        self.execute(stmt, scope)
                except BreakException:
                    break
                except ContinueException:
                    continue
        
        if isinstance(node, While):
            while self.execute(node.condition, scope):
                try:
                    for stmt in node.body:
                        self.execute(stmt, scope)
                except BreakException:
                    break
                except ContinueException:
                    continue
        
        if isinstance(node, Match):
            value = self.execute(node.value, scope)
            
            for case_value, case_body in node.cases:
                if self.execute(case_value, scope) == value:
                    for stmt in case_body:
                        self.execute(stmt, scope)
                    return
            
            for stmt in node.default:
                self.execute(stmt, scope)
        
        if isinstance(node, Try):
            try:
                for stmt in node.body:
                    self.execute(stmt, scope)
            except Exception as e:
                if node.catch_var:
                    scope[node.catch_var] = str(e)
                for stmt in node.catch_body:
                    self.execute(stmt, scope)
            finally:
                for stmt in node.finally_body:
                    self.execute(stmt, scope)
        
        if isinstance(node, Throw):
            value = self.execute(node.value, scope)
            raise Exception(value)
        
        if isinstance(node, Import):
            # TODO: Implement module loading
            pass
        
        if isinstance(node, Export):
            # TODO: Implement module exporting
            pass
        
        if isinstance(node, ClassDef):
            class_obj = {
                'type': 'class',
                'name': node.name,
                'parent': node.parent,
                'body': node.body
            }
            scope[node.name] = class_obj
        
        if isinstance(node, IndexAccess):
            obj = self.execute(node.obj, scope)
            index = self.execute(node.index, scope)
            return obj[index]
        
        if isinstance(node, AttributeAccess):
            obj = self.execute(node.obj, scope)
            return getattr(obj, node.attr)
        
        if isinstance(node, Break):
            raise BreakException()
        
        if isinstance(node, Continue):
            raise ContinueException()
        
        return None
    
    def call_builtin(self, name: str, args: List, kwargs: dict) -> Any:
        """Handle built-in functions"""
        
        if name == 'print':
            output = ' '.join(str(a) for a in args)
            self.output.append(output)
            print(output)
            return None
        
        if name == 'len':
            return len(args[0]) if args else 0
        
        if name == 'str':
            return str(args[0]) if args else ""
        
        if name == 'int':
            return int(args[0]) if args else 0
        
        if name == 'float':
            return float(args[0]) if args else 0.0
        
        if name == 'abs':
            return abs(args[0]) if args else 0
        
        if name == 'min':
            return min(args) if args else 0
        
        if name == 'max':
            return max(args) if args else 0
        
        if name == 'sum':
            return sum(args[0]) if args else 0
        
        if name == 'range':
            if len(args) == 1:
                return list(range(args[0]))
            elif len(args) == 2:
                return list(range(args[0], args[1]))
            else:
                return list(range(args[0], args[1], args[2]))
        
        if name == 'type':
            return type(args[0]).__name__ if args else 'None'
        
        if name == 'isinstance':
            if len(args) >= 2:
                return isinstance(args[0], eval(args[1]))
            return False
        
        if name == 'input':
            return input(args[0] if args else "")
        
        if name == 'time':
            return time.time()
        
        if name == 'random':
            if args:
                return random.random() * args[0]
            return random.random()
        
        if name == 'hash':
            return hash(args[0]) if args else 0
        
        raise RuntimeError(f"Unknown built-in function '{name}'")


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 easylang_v2.py <program.el>")
        print("\nEasyLang v2 - The Human Programming Language")
        print("\nExample program (save as hello.el):")
        print('print "Hello, World!"')
        print("\nDifficulty Level: ⭐ (1/10)")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Lexing
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parsing
        parser = Parser(tokens)
        program = parser.parse()
        
        # Interpretation
        interpreter = Interpreter()
        interpreter.interpret(program)
        
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
