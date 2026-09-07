#!/usr/bin/env python3
"""Tests for HardwareLang"""

import sys
sys.path.insert(0, '../hardwarelang')

from hardwarelang import Lexer, Parser, Interpreter

def test_blink():
    """Test LED blink program"""
    source = '''
# Initialize the board
board arduino = Arduino

# Define the LED
led onboard = LED(pin: GPIO2)

# Main loop
function loop():
  digitalWrite(GPIO2, HIGH)
  delay(500)
  digitalWrite(GPIO2, LOW)
  delay(500)
end
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    print("✓ Blink test passed")

def test_motor_control():
    """Test motor control program"""
    source = '''
# Initialize the board
board esp32 = ESP32

# Define motors
motor left = Motor(pin_fwd: GPIO5, pin_bwd: GPIO6)
motor right = Motor(pin_fwd: GPIO9, pin_bwd: GPIO10)

# Move forward
function moveForward(speed):
  motorControl(left, FWD, speed)
  motorControl(right, FWD, speed)
end

# Move backward
function moveBackward(speed):
  motorControl(left, BWD, speed)
  motorControl(right, BWD, speed)
end

# Turn left
function turnLeft(speed):
  motorControl(left, BWD, speed)
  motorControl(right, FWD, speed)
end

# Turn right
function turnRight(speed):
  motorControl(left, FWD, speed)
  motorControl(right, BWD, speed)
end

# Stop
function stop():
  motorControl(left, STOP, 0)
  motorControl(right, STOP, 0)
end
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    print("✓ Motor control test passed")

def test_sensor_reading():
    """Test sensor reading program"""
    source = '''
# Initialize the board
board raspberry_pi = RaspberryPi

# Define sensors
sensor ultrasonic = Sensor(pin_trig: GPIO17, pin_echo: GPIO18, type: ULTRASONIC)
sensor temperature = Sensor(pin: GPIO27, type: TEMP)

# Read distance
function readDistance():
  digitalWrite(GPIO17, HIGH)
  delay(10)
  digitalWrite(GPIO17, LOW)
  let duration = pulseIn(GPIO18, HIGH)
  let distance = (duration * 0.034) / 2
  return distance
end

# Read temperature
function readTemperature():
  return readADC(GPIO27) * 0.48828125
end
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    print("✓ Sensor reading test passed")

if __name__ == '__main__':
    test_blink()
    test_motor_control()
    test_sensor_reading()
    print("\n✅ All HardwareLang tests passed!")
