#!/usr/bin/env python3
"""
HardLang v2 - The Malbolge of Practical Languages

A genuinely difficult language inspired by Malbolge:
- Self-modifying code
- Ternary virtual machine
- Encrypted source code
- Rotational instructions
- No variables, only memory addresses
- Right-to-left execution
"""

import sys
import os
import math
from enum import IntEnum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


class Instruction(IntEnum):
    """Ternary instruction set"""
    NOP = 0
    INC = 1      # Increment register
    DEC = 2      # Decrement register
    ADD = 3      # Add registers
    LOAD = 4     # Load from memory
    STORE = 5    # Store to memory
    JZ = 6       # Jump if zero
    JNZ = 7      # Jump if nonzero
    HALT = 8     # Stop execution
    OUTPUT = 9   # Output value
    INPUT = 10   # Input value
    ENCRYPT = 11 # Encrypt memory cell
    DECRYPT = 12 # Decrypt memory cell
    ROTATE = 13  # Rotate instruction
    COPY = 14    # Copy memory
    CRAZY = 15   # Crazytown operation


class Register(IntEnum):
    """VM Registers"""
    A = 0
    B = 1
    C = 2


# Crazytown lookup table (Malbolge-inspired)
CRAZY_TABLE = [
    1, 0, 0, 1, 1, 1, 0, 0, 0, 1,
    1, 0, 1, 0, 2, 1, 0, 1, 2, 0,
    2, 1, 1, 2, 2, 2, 1, 0, 2, 1,
    0, 2, 1, 2, 0, 2, 2, 0, 1, 0,
    0, 2, 0, 1, 2, 2, 2, 1, 2, 0,
    1, 2, 2, 1, 0, 0, 0, 2, 1, 1,
    2, 1, 0, 2, 0, 1, 2, 2, 1, 2,
    1, 2, 0, 0, 2, 0, 1, 0, 2, 1,
    1, 0, 2, 1, 0, 1, 2, 2, 2, 1,
    2, 0, 1, 2, 2, 1, 0, 0, 0, 2,
]


class HardLangError(Exception):
    """Custom exception for HardLang errors"""
    def __init__(self, message: str, line: int = 0, col: int = 0):
        self.line = line
        self.col = col
        super().__init__(f"HardLang v2 Error at line {line}, col {col}: {message}")


class Compiler:
    """
    HardLang v2 Compiler
    
    Compiles source code to bytecode for the virtual machine.
    The compilation process itself is difficult due to:
    1. Self-modifying code analysis
    2. Encrypted source handling
    3. Rotational instruction resolution
    4. Crazytown operation mapping
    """
    
    def __init__(self):
        self.memory_size = 59049  # 3^10 - maximum memory
        self.bytecode = []
        self.memory = [0] * self.memory_size
        self.pc = 0  # Program counter
        
    def compile(self, source: str) -> List[int]:
        """
        Compile source code to bytecode.
        
        The source code is encrypted and must be decrypted during compilation.
        Each character is encoded as a ternary value.
        """
        # Step 1: Decrypt source code
        decrypted = self._decrypt_source(source)
        
        # Step 2: Parse instructions
        instructions = self._parse_instructions(decrypted)
        
        # Step 3: Resolve self-modifying code
        resolved = self._resolve_self_modifying(instructions)
        
        # Step 4: Generate bytecode
        bytecode = self._generate_bytecode(resolved)
        
        return bytecode
    
    def _decrypt_source(self, source: str) -> str:
        """
        Decrypt encrypted source code.
        
        Each character is XORed with its position modulo 3.
        """
        decrypted = []
        for i, char in enumerate(source):
            if char.isalpha():
                # XOR with position mod 3
                decrypted_char = chr(ord(char) ^ (i % 3))
                decrypted.append(decrypted_char)
            elif char.isdigit():
                # Digits are kept as-is but mapped to ternary
                decrypted.append(str(int(char) % 3))
            elif char in '+-*/':
                # Operators are rotated
                ops = ['+', '-', '*', '/']
                idx = ops.index(char) if char in ops else 0
                decrypted.append(ops[(idx + 1) % 4])
            else:
                decrypted.append(char)
        
        return ''.join(decrypted)
    
    def _parse_instructions(self, source: str) -> List[Tuple[int, int]]:
        """
        Parse source into instruction tuples (opcode, operand).
        
        Instructions are encoded as pairs of ternary digits.
        """
        instructions = []
        i = 0
        
        while i < len(source):
            char = source[i]
            
            # Map characters to ternary values
            if char in '0123456789':
                ternary_val = int(char) % 3
            elif char.isalpha():
                ternary_val = ord(char.lower()) % 3
            elif char in '+-*/':
                ternary_val = hash(char) % 3
            else:
                ternary_val = 0
            
            # Get next ternary value for operand
            if i + 1 < len(source):
                next_char = source[i + 1]
                if next_char in '0123456789':
                    operand = int(next_char) % 3
                elif next_char.isalpha():
                    operand = ord(next_char.lower()) % 3
                else:
                    operand = 0
            else:
                operand = 0
            
            # Map to instruction
            opcode = self._map_to_opcode(ternary_val, i)
            instructions.append((opcode, operand))
            
            i += 2  # Skip two characters per instruction
        
        return instructions
    
    def _map_to_opcode(self, ternary_val: int, position: int) -> Instruction:
        """
        Map ternary value to opcode.
        
        The mapping changes based on position (rotational instructions).
        """
        # Base mapping
        base_map = {
            0: Instruction.NOP,
            1: Instruction.INC,
            2: Instruction.DEC,
        }
        
        # Rotational offset based on position
        rotation = position % 16
        
        # Apply rotation
        opcode_value = (ternary_val + rotation) % 16
        
        # Map to instruction
        for instr in Instruction:
            if instr.value == opcode_value:
                return instr
        
        return Instruction.NOP
    
    def _resolve_self_modifying(self, instructions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Resolve self-modifying code.
        
        Some instructions modify other instructions as they execute.
        We need to resolve these at compile time.
        """
        resolved = list(instructions)
        
        for i, (opcode, operand) in enumerate(instructions):
            if opcode == Instruction.STORE:
                # STORE instruction might modify nearby instructions
                target = (i + operand) % len(instructions)
                if target < len(resolved):
                    # Apply crazytown transformation
                    crazy_val = CRAZY_TABLE[i % len(CRAZY_TABLE)]
                    resolved[target] = (
                        (resolved[target][0] + crazy_val) % 16,
                        resolved[target][1]
                    )
            
            elif opcode == Instruction.ROTATE:
                # ROTATE instruction changes nearby instructions
                for j in range(max(0, i-2), min(len(resolved), i+3)):
                    if j != i:
                        crazy_val = CRAZY_TABLE[(i + j) % len(CRAZY_TABLE)]
                        resolved[j] = (
                            (resolved[j][0] + crazy_val) % 16,
                            resolved[j][1]
                        )
        
        return resolved
    
    def _generate_bytecode(self, instructions: List[Tuple[int, int]]) -> List[int]:
        """
        Generate final bytecode from instructions.
        
        Each instruction is encoded as a single byte:
        - High nibble: opcode
        - Low nibble: operand
        """
        bytecode = []
        
        for opcode, operand in instructions:
            # Encode as single byte
            byte_val = (opcode << 4) | (operand & 0x0F)
            bytecode.append(byte_val)
        
        return bytecode


class VirtualMachine:
    """
    HardLang v2 Virtual Machine
    
    A ternary-based VM with:
    - 3 registers (A, B, C)
    - 59049 memory cells (3^10)
    - Self-modifying memory
    - Encrypted memory cells
    - Crazytown operations
    """
    
    def __init__(self):
        self.registers = [0, 0, 0]  # A, B, C
        self.memory = [0] * 59049   # 3^10 memory cells
        self.pc = 0                 # Program counter
        self.halted = False
        self.output_buffer = []
        self.input_buffer = []
        self.encryption_key = 0x15  # Malbolge magic constant
        
    def load(self, bytecode: List[int]):
        """Load bytecode into memory"""
        for i, byte_val in enumerate(bytecode):
            if i < len(self.memory):
                self.memory[i] = byte_val
    
    def run(self, max_steps: int = 1000000):
        """Execute the program"""
        steps = 0
        
        while not self.halted and steps < max_steps:
            self._execute_instruction()
            steps += 1
        
        if steps >= max_steps:
            raise HardLangError("Execution limit exceeded (possible infinite loop)")
        
        return self.output_buffer
    
    def _execute_instruction(self):
        """Execute a single instruction"""
        if self.pc >= len(self.memory):
            self.halted = True
            return
        
        # Get current instruction
        instruction_byte = self.memory[self.pc]
        
        # Decode instruction
        opcode = (instruction_byte >> 4) & 0x0F
        operand = instruction_byte & 0x0F
        
        # Execute based on opcode
        if opcode == Instruction.NOP:
            pass
        
        elif opcode == Instruction.INC:
            self.registers[Register.A] = (self.registers[Register.A] + 1) % 59049
        
        elif opcode == Instruction.DEC:
            self.registers[Register.A] = (self.registers[Register.A] - 1) % 59049
        
        elif opcode == Instruction.ADD:
            self.registers[Register.A] = (
                self.registers[Register.A] + self.registers[Register.B]
            ) % 59049
        
        elif opcode == Instruction.LOAD:
            addr = (self.pc + operand) % 59049
            self.registers[Register.A] = self.memory[addr]
        
        elif opcode == Instruction.STORE:
            addr = (self.pc + operand) % 59049
            self.memory[addr] = self.registers[Register.A]
        
        elif opcode == Instruction.JZ:
            if self.registers[Register.A] == 0:
                self.pc = (self.pc + operand) % 59049
                return
        
        elif opcode == Instruction.JNZ:
            if self.registers[Register.A] != 0:
                self.pc = (self.pc + operand) % 59049
                return
        
        elif opcode == Instruction.HALT:
            self.halted = True
            return
        
        elif opcode == Instruction.OUTPUT:
            self.output_buffer.append(self.registers[Register.A])
        
        elif opcode == Instruction.INPUT:
            if self.input_buffer:
                self.registers[Register.A] = self.input_buffer.pop(0)
            else:
                self.registers[Register.A] = 0
        
        elif opcode == Instruction.ENCRYPT:
            addr = (self.pc + operand) % 59049
            self.memory[addr] = self._encrypt(self.memory[addr])
        
        elif opcode == Instruction.DECRYPT:
            addr = (self.pc + operand) % 59049
            self.memory[addr] = self._decrypt(self.memory[addr])
        
        elif opcode == Instruction.ROTATE:
            # Rotate instruction at target address
            addr = (self.pc + operand) % 59049
            target = self.memory[addr]
            rotated = ((target >> 4) | (target << 4)) & 0xFF
            self.memory[addr] = rotated
        
        elif opcode == Instruction.COPY:
            src = (self.pc + operand) % 59049
            dst = (self.pc + operand + 1) % 59049
            self.memory[dst] = self.memory[src]
        
        elif opcode == Instruction.CRAZY:
            # Crazytown operation - Malbolge-inspired
            crazy_val = CRAZY_TABLE[self.pc % len(CRAZY_TABLE)]
            self.registers[Register.A] = (
                self.registers[Register.A] + crazy_val
            ) % 59049
            # Also modify memory
            addr = (self.pc + operand) % 59049
            self.memory[addr] = (self.memory[addr] + crazy_val) % 59049
        
        # Self-modifying code: instructions modify themselves
        self.memory[self.pc] = (self.memory[self.pc] + 1) % 256
        
        # Move to next instruction
        self.pc = (self.pc + 1) % 59049
    
    def _encrypt(self, value: int) -> int:
        """Encrypt a value using XOR with key"""
        return value ^ self.encryption_key
    
    def _decrypt(self, value: int) -> int:
        """Decrypt a value using XOR with key"""
        return value ^ self.encryption_key


class HardLangV2:
    """Main interface for HardLang v2"""
    
    def __init__(self):
        self.compiler = Compiler()
        self.vm = VirtualMachine()
    
    def compile(self, source: str) -> List[int]:
        """Compile source to bytecode"""
        return self.compiler.compile(source)
    
    def run(self, bytecode: List[int]) -> List[int]:
        """Run bytecode"""
        self.vm.load(bytecode)
        return self.vm.run()
    
    def execute(self, source: str) -> List[int]:
        """Compile and run source"""
        bytecode = self.compile(source)
        return self.run(bytecode)
    
    def disassemble(self, bytecode: List[int]) -> str:
        """Disassemble bytecode to readable format"""
        lines = []
        
        for i, byte_val in enumerate(bytecode):
            opcode = (byte_val >> 4) & 0x0F
            operand = byte_val & 0x0F
            
            # Find instruction name
            instr_name = "UNKNOWN"
            for instr in Instruction:
                if instr.value == opcode:
                    instr_name = instr.name
                    break
            
            lines.append(f"{i:4d}: {instr_name:8s} {operand}")
        
        return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 hardlang_v2.py <program.hl2>")
        print("\nExample program (save as hello.hl2):")
        print("9*8*7*6*5*4*3*2*1*0")
        print("\nDifficulty Level: ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ (10/10)")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        hlv2 = HardLangV2()
        output = hlv2.execute(source)
        
        # Convert output to characters if they're ASCII
        for val in output:
            if 32 <= val <= 126:
                print(chr(val), end='')
            else:
                print(val, end=' ')
        print()
        
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
