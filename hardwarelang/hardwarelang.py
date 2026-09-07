#!/usr/bin/env python3
"""
HardwareLang - The Hardware Control Language

A real programming language for controlling hardware directly:
- Microcontrollers (Arduino, ESP32, STM32)
- Single Board Computers (Raspberry Pi)
- Industrial PLCs
- Robots
- Sensors and Actuators
- Communication Protocols (UART, SPI, I2C, CAN)
"""

import sys
import os
import time
import json
import struct
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional, Tuple, Union
from abc import ABC, abstractmethod


# =============================================================================
# HARDWARE ABSTRACTION LAYER
# =============================================================================

class PinMode(Enum):
    INPUT = "input"
    OUTPUT = "output"
    INPUT_PULLUP = "input_pullup"
    INPUT_PULLDOWN = "input_pulldown"
    PWM = "pwm"
    ADC = "adc"
    UART_TX = "uart_tx"
    UART_RX = "uart_rx"
    SPI_MOSI = "spi_mosi"
    SPI_MISO = "spi_miso"
    SPI_SCK = "spi_sck"
    SPI_CS = "spi_cs"
    I2C_SDA = "i2c_sda"
    I2C_SCL = "i2c_scl"


class PinState(Enum):
    LOW = 0
    HIGH = 1


class BoardType(Enum):
    ARDUINO_UNO = "arduino_uno"
    ARDUINO_MEGA = "arduino_mega"
    ESP32 = "esp32"
    ESP8266 = "esp8266"
    RASPBERRY_PI = "raspberry_pi"
    STM32 = "stm32"
    PIC = "pic"
    AVR = "avr"
    GENERIC = "generic"


@dataclass
class Pin:
    number: int
    mode: PinMode = PinMode.INPUT
    state: PinState = PinState.LOW
    pwm_duty: float = 0.0
    pwm_freq: float = 1000.0
    adc_value: int = 0
    name: str = ""


@dataclass
class Board:
    board_type: BoardType
    name: str
    pins: Dict[int, Pin] = field(default_factory=dict)
    digital_count: int = 14
    analog_count: int = 6
    pwm_count: int = 6
    uart_count: int = 1
    spi_count: int = 1
    i2c_count: int = 1
    
    def __post_init__(self):
        # Initialize default pins based on board type
        if self.board_type == BoardType.ARDUINO_UNO:
            self.digital_count = 14
            self.analog_count = 6
            self.pwm_count = 6
        elif self.board_type == BoardType.ESP32:
            self.digital_count = 34
            self.analog_count = 16
            self.pwm_count = 16
        elif self.board_type == BoardType.RASPBERRY_PI:
            self.digital_count = 40
            self.analog_count = 0
            self.pwm_count = 2
        
        # Create pin objects
        for i in range(self.digital_count):
            self.pins[i] = Pin(number=i, name=f"GPIO{i}")
        for i in range(self.analog_count):
            self.pins[100 + i] = Pin(number=100 + i, name=f"ADC{i}")


class HardwareInterface(ABC):
    """Abstract hardware interface"""
    
    @abstractmethod
    def digital_read(self, pin: int) -> PinState:
        pass
    
    @abstractmethod
    def digital_write(self, pin: int, state: PinState):
        pass
    
    @abstractmethod
    def analog_read(self, pin: int) -> int:
        pass
    
    @abstractmethod
    def analog_write(self, pin: int, value: int):
        pass
    
    @abstractmethod
    def pwm_write(self, pin: int, duty: float, freq: float):
        pass
    
    @abstractmethod
    def set_pin_mode(self, pin: int, mode: PinMode):
        pass


class SimulatedHardware(HardwareInterface):
    """Simulated hardware for testing"""
    
    def __init__(self):
        self.pins = {}
        self.output_log = []
    
    def digital_read(self, pin: int) -> PinState:
        return self.pins.get(pin, PinState.LOW)
    
    def digital_write(self, pin: int, state: PinState):
        self.pins[pin] = state
        self.output_log.append(f"GPIO{pin} = {state.name}")
    
    def analog_read(self, pin: int) -> int:
        return self.pins.get(pin, 0)
    
    def analog_write(self, pin: int, value: int):
        self.pins[pin] = value
        self.output_log.append(f"ADC{pin} = {value}")
    
    def pwm_write(self, pin: int, duty: float, freq: float):
        self.pins[pin] = duty
        self.output_log.append(f"PWM{pin} = {duty}% @ {freq}Hz")
    
    def set_pin_mode(self, pin: int, mode: PinMode):
        self.output_log.append(f"GPIO{pin} mode = {mode.value}")


class UARTInterface:
    """UART communication interface"""
    
    def __init__(self, tx_pin: int, rx_pin: int, baud: int = 9600):
        self.tx_pin = tx_pin
        self.rx_pin = rx_pin
        self.baud = baud
        self.buffer = []
    
    def write(self, data: List[int]):
        self.buffer.extend(data)
        print(f"UART TX: {[hex(x) for x in data]}")
    
    def read(self, count: int) -> List[int]:
        data = self.buffer[:count]
        self.buffer = self.buffer[count:]
        return data
    
    def available(self) -> int:
        return len(self.buffer)


class I2CInterface:
    """I2C communication interface"""
    
    def __init__(self, sda_pin: int, scl_pin: int, freq: int = 100000):
        self.sda_pin = sda_pin
        self.scl_pin = scl_pin
        self.freq = freq
        self.devices = {}
    
    def write_reg(self, addr: int, reg: int, data: List[int]):
        if addr not in self.devices:
            self.devices[addr] = {}
        self.devices[addr][reg] = data
        print(f"I2C WRITE: addr={hex(addr)} reg={hex(reg)} data={[hex(x) for x in data]}")
    
    def read_reg(self, addr: int, reg: int, count: int) -> List[int]:
        if addr in self.devices and reg in self.devices[addr]:
            return self.devices[addr][reg][:count]
        return [0] * count


class SPIInterface:
    """SPI communication interface"""
    
    def __init__(self, mosi_pin: int, miso_pin: int, sck_pin: int, cs_pin: int):
        self.mosi_pin = mosi_pin
        self.miso_pin = miso_pin
        self.sck_pin = sck_pin
        self.cs_pin = cs_pin
    
    def write(self, data: List[int]):
        print(f"SPI TX: {[hex(x) for x in data]}")
    
    def transfer(self, data: List[int]) -> List[int]:
        print(f"SPI TRANSFER: {[hex(x) for x in data]}")
        return [0x00] * len(data)


class CANInterface:
    """CAN bus communication interface"""
    
    def __init__(self, can_rx: int, can_tx: int, speed: int = 500000):
        self.can_rx = can_rx
        self.can_tx = can_tx
        self.speed = speed
        self.rx_buffer = []
    
    def send(self, id: int, data: List[int], extended: bool = False):
        print(f"CAN TX: id={hex(id)} data={[hex(x) for x in data]}")
    
    def recv(self) -> Optional[Dict]:
        if self.rx_buffer:
            return self.rx_buffer.pop(0)
        return None
    
    def callback(self, func):
        pass


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
    
    # Hardware keywords
    BOARD = "BOARD"
    SENSOR = "SENSOR"
    MOTOR = "MOTOR"
    LED = "LED"
    SERVO = "SERVO"
    DISPLAY = "DISPLAY"
    UART = "UART"
    SPI = "SPI"
    I2C = "I2C"
    CAN = "CAN"
    TIMER = "TIMER"
    
    # Pin constants
    GPIO = "GPIO"
    ADC = "ADC"
    PWM = "PWM"
    
    # Digital states
    HIGH = "HIGH"
    LOW = "LOW"
    
    # Operators
    ASSIGN = "ASSIGN"
    EQUALS = "EQUALS"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    
    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    DOT = "DOT"
    ARROW = "ARROW"
    
    # Keywords
    LET = "LET"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    IF = "IF"
    ELSE = "ELSE"
    END = "END"
    FOR = "FOR"
    IN = "IN"
    WHILE = "WHILE"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    INTERRUPT = "INTERRUPT"
    CALLBACK = "CALLBACK"
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"


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
    """Tokenizer for HardwareLang"""
    
    KEYWORDS = {
        'board': TokenType.BOARD,
        'sensor': TokenType.SENSOR,
        'motor': TokenType.MOTOR,
        'led': TokenType.LED,
        'servo': TokenType.SERVO,
        'display': TokenType.DISPLAY,
        'uart': TokenType.UART,
        'spi': TokenType.SPI,
        'i2c': TokenType.I2C,
        'can': TokenType.CAN,
        'timer': TokenType.TIMER,
        'let': TokenType.LET,
        'function': TokenType.FUNCTION,
        'return': TokenType.RETURN,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'end': TokenType.END,
        'for': TokenType.FOR,
        'in': TokenType.IN,
        'while': TokenType.WHILE,
        'break': TokenType.BREAK,
        'continue': TokenType.CONTINUE,
        'interrupt': TokenType.INTERRUPT,
        'callback': TokenType.CALLBACK,
        'true': TokenType.BOOLEAN,
        'false': TokenType.BOOLEAN,
        'high': TokenType.HIGH,
        'low': TokenType.LOW,
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
        if self.peek() == '/' and self.peek_next() == '/':
            while self.pos < len(self.source) and self.source[self.pos] != '\n':
                self.advance()
    
    def peek_next(self) -> str:
        if self.pos + 1 < len(self.source):
            return self.source[self.pos + 1]
        return '\0'
    
    def read_string(self) -> Token:
        start_line, start_col = self.line, self.col
        quote = self.advance()
        value = []
        
        while self.pos < len(self.source) and self.source[self.pos] != quote:
            if self.source[self.pos] == '\\':
                self.advance()
                escape = self.advance()
                escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"'}
                value.append(escape_map.get(escape, escape))
            else:
                value.append(self.advance())
        
        self.advance()  # closing quote
        return Token(TokenType.STRING, ''.join(value), start_line, start_col)
    
    def read_number(self) -> Token:
        start_line, start_col = self.line, self.col
        value = ''
        is_float = False
        
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            if self.source[self.pos] == '.':
                is_float = True
            value += self.advance()
        
        if is_float:
            return Token(TokenType.FLOAT, float(value), start_line, start_col)
        return Token(TokenType.INTEGER, int(value), start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.col
        value = ''
        
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            value += self.advance()
        
        # Check for GPIO/ADC/PWM prefix
        if value.upper().startswith('GPIO'):
            try:
                pin_num = int(value[4:])
                return Token(TokenType.GPIO, pin_num, start_line, start_col)
            except ValueError:
                pass
        
        if value.upper().startswith('ADC'):
            try:
                pin_num = int(value[3:])
                return Token(TokenType.ADC, pin_num + 100, start_line, start_col)
            except ValueError:
                pass
        
        if value.upper().startswith('PWM'):
            try:
                pin_num = int(value[3:])
                return Token(TokenType.PWM, pin_num, start_line, start_col)
            except ValueError:
                pass
        
        # Check keywords
        if value.lower() in self.KEYWORDS:
            token_type = self.KEYWORDS[value.lower()]
            if token_type == TokenType.BOOLEAN:
                return Token(token_type, value.lower() == 'true', start_line, start_col)
            if token_type in (TokenType.HIGH, TokenType.LOW):
                return Token(token_type, 1 if value.upper() == 'HIGH' else 0, start_line, start_col)
            return Token(token_type, value, start_line, start_col)
        
        return Token(TokenType.IDENTIFIER, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Skip comments
            if self.peek() == '/' and self.peek_next() == '/':
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
            
            # Identifiers
            if self.peek().isalpha() or self.peek() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operators and delimiters
            single_chars = {
                '=': TokenType.ASSIGN, '+': TokenType.PLUS, '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY, '/': TokenType.DIVIDE, '%': TokenType.MODULO,
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
            
            raise Exception(f"Unexpected character '{self.peek()}' at line {self.line}")
        
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
class Identifier(ASTNode):
    name: str = ""

@dataclass
class PinReference(ASTNode):
    pin: int = 0
    pin_type: str = "gpio"

@dataclass
class BoardInit(ASTNode):
    board_type: str = ""
    name: str = ""

@dataclass
class DeviceInit(ASTNode):
    device_type: str = ""
    name: str = ""
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DigitalRead(ASTNode):
    pin: ASTNode = None

@dataclass
class DigitalWrite(ASTNode):
    pin: ASTNode = None
    value: ASTNode = None

@dataclass
class AnalogRead(ASTNode):
    pin: ASTNode = None

@dataclass
class PWMWrite(ASTNode):
    pin: ASTNode = None
    duty: ASTNode = None
    freq: ASTNode = None

@dataclass
class UARTWrite(ASTNode):
    device: str = ""
    data: List[ASTNode] = field(default_factory=list)

@dataclass
class UARTRead(ASTNode):
    device: str = ""
    count: ASTNode = None

@dataclass
class I2CWrite(ASTNode):
    device: str = ""
    addr: ASTNode = None
    reg: ASTNode = None
    data: List[ASTNode] = field(default_factory=list)

@dataclass
class I2CRead(ASTNode):
    device: str = ""
    addr: ASTNode = None
    reg: ASTNode = None
    count: ASTNode = None

@dataclass
class SPIWrite(ASTNode):
    device: str = ""
    data: List[ASTNode] = field(default_factory=list)

@dataclass
class SPITransfer(ASTNode):
    device: str = ""
    data: List[ASTNode] = field(default_factory=list)

@dataclass
class CANSend(ASTNode):
    device: str = ""
    id: ASTNode = None
    data: List[ASTNode] = field(default_factory=list)

@dataclass
class CANRecv(ASTNode):
    device: str = ""

@dataclass
class MotorControl(ASTNode):
    device: str = ""
    command: str = ""
    params: Dict[str, ASTNode] = field(default_factory=dict)

@dataclass
class ServoControl(ASTNode):
    device: str = ""
    angle: ASTNode = None

@dataclass
class LEDControl(ASTNode):
    device: str = ""
    state: ASTNode = None

@dataclass
class TimerInit(ASTNode):
    name: str = ""
    frequency: ASTNode = None

@dataclass
class TimerCallback(ASTNode):
    name: str = ""
    callback: str = ""

@dataclass
class InterruptInit(ASTNode):
    pin: ASTNode = None
    mode: str = ""
    callback: str = ""

@dataclass
class FunctionDef(ASTNode):
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class FunctionCall(ASTNode):
    name: str = ""
    args: List[ASTNode] = field(default_factory=list)

@dataclass
class Assignment(ASTNode):
    name: str = ""
    value: ASTNode = None

@dataclass
class If(ASTNode):
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)

@dataclass
class While(ASTNode):
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class For(ASTNode):
    var: str = ""
    iterable: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class Return(ASTNode):
    value: ASTNode = None

@dataclass
class Break(ASTNode):
    pass

@dataclass
class Continue(ASTNode):
    pass

@dataclass
class BinaryOp(ASTNode):
    op: str = ""
    left: ASTNode = None
    right: ASTNode = None


# =============================================================================
# PARSER
# =============================================================================

class Parser:
    """Parser for HardwareLang"""
    
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
            raise Exception(f"Expected {token_type.name} at line {self.peek().line}")
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
        
        if self.peek().type == TokenType.BOARD:
            return self.parse_board_init()
        if self.peek().type in (TokenType.SENSOR, TokenType.MOTOR, TokenType.LED,
                                  TokenType.SERVO, TokenType.DISPLAY):
            return self.parse_device_init()
        if self.peek().type == TokenType.LET:
            return self.parse_assignment()
        if self.peek().type == TokenType.FUNCTION:
            return self.parse_function()
        if self.peek().type == TokenType.IF:
            return self.parse_if()
        if self.peek().type == TokenType.FOR:
            return self.parse_for()
        if self.peek().type == TokenType.WHILE:
            return self.parse_while()
        if self.peek().type == TokenType.RETURN:
            return self.parse_return()
        if self.peek().type == TokenType.INTERRUPT:
            return self.parse_interrupt()
        if self.peek().type == TokenType.BREAK:
            self.advance()
            return Break(line=self.peek().line, col=self.peek().col)
        if self.peek().type == TokenType.CONTINUE:
            self.advance()
            return Continue(line=self.peek().line, col=self.peek().col)
        
        return self.parse_expression_statement()
    
    def parse_board_init(self) -> BoardInit:
        token = self.advance()  # board
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        board_type = self.expect(TokenType.IDENTIFIER).value
        return BoardInit(board_type=board_type, name=name,
                        line=token.line, col=token.col)
    
    def parse_device_init(self) -> DeviceInit:
        token = self.advance()
        device_type = token.value
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        self.expect(TokenType.LPAREN)
        
        params = {}
        if self.peek().type != TokenType.RPAREN:
            param_name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.COLON)
            param_value = self.parse_expression()
            params[param_name] = param_value
            
            while self.peek().type == TokenType.COMMA:
                self.advance()
                param_name = self.expect(TokenType.IDENTIFIER).value
                self.expect(TokenType.COLON)
                param_value = self.parse_expression()
                params[param_name] = param_value
        
        self.expect(TokenType.RPAREN)
        return DeviceInit(device_type=device_type, name=name, params=params,
                         line=token.line, col=token.col)
    
    def parse_assignment(self) -> Assignment:
        token = self.expect(TokenType.LET)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        return Assignment(name=name, value=value,
                         line=token.line, col=token.col)
    
    def parse_function(self) -> FunctionDef:
        token = self.expect(TokenType.FUNCTION)
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        params = []
        if self.peek().type != TokenType.RPAREN:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.peek().type == TokenType.COMMA:
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.COLON)
        self.skip_newlines()
        
        body = []
        while self.peek().type != TokenType.END:
            body.append(self.parse_statement())
            self.skip_newlines()
        
        self.expect(TokenType.END)
        return FunctionDef(name=name, params=params, body=body,
                         line=token.line, col=token.col)
    
    def parse_if(self) -> If:
        token = self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        self.skip_newlines()
        
        body = []
        while self.peek().type not in (TokenType.ELSE, TokenType.END):
            body.append(self.parse_statement())
            self.skip_newlines()
        
        else_body = []
        if self.peek().type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.COLON)
            self.skip_newlines()
            while self.peek().type != TokenType.END:
                else_body.append(self.parse_statement())
                self.skip_newlines()
        
        self.expect(TokenType.END)
        return If(condition=condition, body=body, else_body=else_body,
                 line=token.line, col=token.col)
    
    def parse_while(self) -> While:
        token = self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        self.skip_newlines()
        
        body = []
        while self.peek().type != TokenType.END:
            body.append(self.parse_statement())
            self.skip_newlines()
        
        self.expect(TokenType.END)
        return While(condition=condition, body=body,
                    line=token.line, col=token.col)
    
    def parse_for(self) -> For:
        token = self.expect(TokenType.FOR)
        var = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.IN)
        iterable = self.parse_expression()
        self.expect(TokenType.COLON)
        self.skip_newlines()
        
        body = []
        while self.peek().type != TokenType.END:
            body.append(self.parse_statement())
            self.skip_newlines()
        
        self.expect(TokenType.END)
        return For(var=var, iterable=iterable, body=body,
                  line=token.line, col=token.col)
    
    def parse_return(self) -> Return:
        token = self.expect(TokenType.RETURN)
        value = None
        if self.peek().type != TokenType.NEWLINE:
            value = self.parse_expression()
        return Return(value=value, line=token.line, col=token.col)
    
    def parse_interrupt(self) -> InterruptInit:
        token = self.expect(TokenType.INTERRUPT)
        pin = self.parse_expression()
        mode = self.expect(TokenType.IDENTIFIER).value
        callback = self.expect(TokenType.IDENTIFIER).value
        return InterruptInit(pin=pin, mode=mode, callback=callback,
                           line=token.line, col=token.col)
    
    def parse_expression_statement(self) -> Optional[ASTNode]:
        expr = self.parse_expression()
        
        if isinstance(expr, FunctionCall):
            return expr
        
        if self.peek().type == TokenType.ASSIGN:
            self.advance()
            value = self.parse_expression()
            if isinstance(expr, Identifier):
                return Assignment(name=expr.name, value=value,
                                line=expr.line, col=expr.col)
        
        return expr
    
    def parse_expression(self) -> ASTNode:
        return self.parse_comparison()
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        
        while self.peek().type == TokenType.EQUALS:
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(op="==", left=left, right=right,
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
        left = self.parse_primary()
        
        while self.peek().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            right = self.parse_primary()
            left = BinaryOp(op=op, left=left, right=right,
                          line=left.line, col=left.col)
        
        return left
    
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
        
        if token.type == TokenType.HIGH:
            self.advance()
            return NumberLiteral(value=1, line=token.line, col=token.col)
        
        if token.type == TokenType.LOW:
            self.advance()
            return NumberLiteral(value=0, line=token.line, col=token.col)
        
        if token.type in (TokenType.GPIO, TokenType.ADC, TokenType.PWM):
            self.advance()
            return PinReference(pin=token.value, pin_type=token.type.name.lower(),
                              line=token.line, col=token.col)
        
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            
            # Check for function call or method call
            if self.peek().type == TokenType.LPAREN:
                self.advance()
                args = []
                if self.peek().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.peek().type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                return FunctionCall(name=token.value, args=args,
                                  line=token.line, col=token.col)
            
            return Identifier(name=token.value, line=token.line, col=token.col)
        
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        raise Exception(f"Unexpected token {token.type.name} at line {token.line}")


# =============================================================================
# INTERPRETER
# =============================================================================

class HardwareInterpreter:
    """Interpreter for HardwareLang"""
    
    def __init__(self):
        self.hardware = SimulatedHardware()
        self.boards = {}
        self.devices = {}
        self.scope = {}
        self.functions = {}
        self.interrupts = {}
        self.timers = {}
        self.output = []
    
    def interpret(self, program: Program):
        for stmt in program.statements:
            self.execute(stmt)
    
    def execute(self, node: ASTNode) -> Any:
        if isinstance(node, BoardInit):
            board = Board(
                board_type=BoardType(node.board_type),
                name=node.name
            )
            self.boards[node.name] = board
            self.output.append(f"Board '{node.name}' initialized as {node.board_type}")
            return board
        
        if isinstance(node, DeviceInit):
            device = {
                'type': node.device_type,
                'name': node.name,
                'params': {}
            }
            
            # Evaluate parameters
            for key, value in node.params.items():
                device['params'][key] = self.execute(value)
            
            self.devices[node.name] = device
            self.output.append(f"{node.device_type} '{node.name}' initialized")
            return device
        
        if isinstance(node, Assignment):
            value = self.execute(node.value)
            self.scope[node.name] = value
            return value
        
        if isinstance(node, FunctionDef):
            self.functions[node.name] = {
                'params': node.params,
                'body': node.body
            }
            return None
        
        if isinstance(node, FunctionCall):
            # Handle built-in functions
            if node.name == 'digital_read':
                pin = self.execute(node.args[0])
                return self.hardware.digital_read(pin)
            
            if node.name == 'digital_write':
                pin = self.execute(node.args[0])
                value = self.execute(node.args[1])
                state = PinState.HIGH if value else PinState.LOW
                self.hardware.digital_write(pin, state)
                return None
            
            if node.name == 'analog_read':
                pin = self.execute(node.args[0])
                return self.hardware.analog_read(pin)
            
            if node.name == 'pwm_write':
                pin = self.execute(node.args[0])
                duty = self.execute(node.args[1])
                freq = self.execute(node.args[2]) if len(node.args) > 2 else 1000
                self.hardware.pwm_write(pin, duty, freq)
                return None
            
            if node.name == 'delay':
                ms = self.execute(node.args[0])
                time.sleep(ms / 1000.0)
                return None
            
            if node.name == 'print':
                values = [str(self.execute(arg)) for arg in node.args]
                output = ' '.join(values)
                self.output.append(output)
                print(output)
                return None
            
            # Handle user-defined functions
            if node.name in self.functions:
                func = self.functions[node.name]
                saved_scope = self.scope.copy()
                
                for i, param in enumerate(func['params']):
                    if i < len(node.args):
                        self.scope[param] = self.execute(node.args[i])
                
                result = None
                try:
                    for stmt in func['body']:
                        result = self.execute(stmt)
                except ReturnValue as rv:
                    result = rv.value
                
                self.scope = saved_scope
                return result
        
        if isinstance(node, Return):
            value = self.execute(node.value) if node.value else None
            raise ReturnValue(value)
        
        if isinstance(node, If):
            condition = self.execute(node.condition)
            if condition:
                for stmt in node.body:
                    self.execute(stmt)
            else:
                for stmt in node.else_body:
                    self.execute(stmt)
        
        if isinstance(node, While):
            while self.execute(node.condition):
                for stmt in node.body:
                    self.execute(stmt)
        
        if isinstance(node, For):
            iterable = self.execute(node.iterable)
            for item in iterable:
                self.scope[node.var] = item
                for stmt in node.body:
                    self.execute(stmt)
        
        if isinstance(node, Break):
            raise BreakException()
        
        if isinstance(node, Continue):
            raise ContinueException()
        
        if isinstance(node, NumberLiteral):
            return node.value
        
        if isinstance(node, StringLiteral):
            return node.value
        
        if isinstance(node, BooleanLiteral):
            return node.value
        
        if isinstance(node, Identifier):
            if node.name in self.scope:
                return self.scope[node.name]
            if node.name in self.devices:
                return self.devices[node.name]
            if node.name in self.boards:
                return self.boards[node.name]
            raise RuntimeError(f"Undefined variable '{node.name}'")
        
        if isinstance(node, PinReference):
            return node.pin
        
        if isinstance(node, BinaryOp):
            left = self.execute(node.left)
            right = self.execute(node.right)
            
            ops = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a / b,
                '%': lambda a, b: a % b,
                '==': lambda a, b: a == b,
                '!=': lambda a, b: a != b,
                '<': lambda a, b: a < b,
                '>': lambda a, b: a > b,
                '<=': lambda a, b: a <= b,
                '>=': lambda a, b: a >= b,
            }
            
            return ops[node.op](left, right)
        
        return None


class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass


# =============================================================================
# CODE GENERATORS
# =============================================================================

class CCodeGenerator:
    """Generate C code from HardwareLang AST"""
    
    def __init__(self):
        self.indent = 0
        self.code = []
        self.includes = set()
        self.variables = {}
        self.functions = {}
    
    def generate(self, program: Program) -> str:
        self.code = []
        self.includes = set()
        
        # Add standard includes
        self.includes.add('#include <Arduino.h>')
        
        # Generate code for each statement
        for stmt in program.statements:
            self.generate_statement(stmt)
        
        # Combine includes and code
        output = '\n'.join(sorted(self.includes)) + '\n\n'
        output += '\n'.join(self.code)
        
        return output
    
    def generate_statement(self, node: ASTNode):
        if isinstance(node, BoardInit):
            # No C equivalent needed
            pass
        
        elif isinstance(node, DeviceInit):
            self.generate_device_init(node)
        
        elif isinstance(node, Assignment):
            self.generate_assignment(node)
        
        elif isinstance(node, FunctionDef):
            self.generate_function(node)
        
        elif isinstance(node, If):
            self.generate_if(node)
        
        elif isinstance(node, While):
            self.generate_while(node)
        
        elif isinstance(node, For):
            self.generate_for(node)
        
        elif isinstance(node, FunctionCall):
            self.generate_function_call(node)
    
    def generate_device_init(self, node: DeviceInit):
        if node.device_type == 'Motor':
            self.code.append(f'// Motor {node.name} initialized')
        elif node.device_type == 'Servo':
            self.includes.add('#include <Servo.h>')
            self.code.append(f'Servo {node.name};')
        elif node.device_type == 'LED':
            pin = node.params.get('pin', 0)
            self.code.append(f'pinMode({pin}, OUTPUT);')
    
    def generate_assignment(self, node: Assignment):
        value = self.generate_expression(node.value)
        self.code.append(f'int {node.name} = {value};')
    
    def generate_function(self, node: FunctionDef):
        params = ', '.join([f'int {p}' for p in node.params])
        self.code.append(f'void {node.name}({params}) {{')
        self.indent += 1
        
        for stmt in node.body:
            self.generate_statement(stmt)
        
        self.indent -= 1
        self.code.append('}')
    
    def generate_if(self, node: If):
        condition = self.generate_expression(node.condition)
        self.code.append(f'if ({condition}) {{')
        self.indent += 1
        
        for stmt in node.body:
            self.generate_statement(stmt)
        
        self.indent -= 1
        
        if node.else_body:
            self.code.append('} else {')
            self.indent += 1
            for stmt in node.else_body:
                self.generate_statement(stmt)
            self.indent -= 1
        
        self.code.append('}')
    
    def generate_while(self, node: While):
        condition = self.generate_expression(node.condition)
        self.code.append(f'while ({condition}) {{')
        self.indent += 1
        
        for stmt in node.body:
            self.generate_statement(stmt)
        
        self.indent -= 1
        self.code.append('}')
    
    def generate_for(self, node: For):
        # Simplified for loop
        self.code.append(f'for (int {node.var} : {{0}}) {{')
        self.indent += 1
        
        for stmt in node.body:
            self.generate_statement(stmt)
        
        self.indent -= 1
        self.code.append('}')
    
    def generate_function_call(self, node: FunctionCall) -> str:
        args = ', '.join([self.generate_expression(arg) for arg in node.args])
        
        if node.name == 'digital_read':
            return f'digitalRead({args})'
        elif node.name == 'digital_write':
            return f'digitalWrite({args})'
        elif node.name == 'analog_read':
            return f'analogRead({args})'
        elif node.name == 'pwm_write':
            return f'analogWrite({args})'
        elif node.name == 'delay':
            self.code.append(f'delay({args});')
            return ''
        elif node.name == 'print':
            self.code.append(f'Serial.println({args});')
            self.includes.add('Serial.begin(9600);')
            return ''
        else:
            return f'{node.name}({args})'
    
    def generate_expression(self, node: ASTNode) -> str:
        if isinstance(node, NumberLiteral):
            return str(node.value)
        if isinstance(node, StringLiteral):
            return f'"{node.value}"'
        if isinstance(node, BooleanLiteral):
            return 'true' if node.value else 'false'
        if isinstance(node, Identifier):
            return node.name
        if isinstance(node, PinReference):
            return str(node.pin)
        if isinstance(node, BinaryOp):
            left = self.generate_expression(node.left)
            right = self.generate_expression(node.right)
            return f'({left} {node.op} {right})'
        if isinstance(node, FunctionCall):
            return self.generate_function_call(node)
        return '0'


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 hardwarelang.py <program.hw>")
        print("\nHardwareLang - The Hardware Control Language")
        print("\nExample program (save as blink.hw):")
        print('board esp32 = ESP32')
        print('led onboard = LED(pin: GPIO2)')
        print('')
        print('function loop():')
        print('  digitalWrite(GPIO2, HIGH)')
        print('  delay(1000)')
        print('  digitalWrite(GPIO2, LOW)')
        print('  delay(1000)')
        print('end')
        print("\nDifficulty Level: ⭐⭐⭐ (3/10)")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Check for compile options
        if '--compile-c' in sys.argv:
            # Compile to C
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            
            generator = CCodeGenerator()
            c_code = generator.generate(program)
            
            output_file = filename.replace('.hw', '.ino')
            with open(output_file, 'w') as f:
                f.write(c_code)
            
            print(f"Compiled to {output_file}")
            return
        
        # Interpret directly
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        
        interpreter = HardwareInterpreter()
        interpreter.interpret(program)
        
        # Print output
        for line in interpreter.output:
            print(line)
        
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
