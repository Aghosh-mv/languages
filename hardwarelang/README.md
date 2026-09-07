# HardwareLang - The Hardware Control Language

## Philosophy
HardwareLang is a **real programming language** for controlling hardware directly.
Not just software - it controls:

1. **Microcontrollers**: Arduino, ESP32, STM32, PIC, AVR
2. **Single Board Computers**: Raspberry Pi, BeagleBone, Odroid
3. **FPGA**: Xilinx, Altera, Lattice
4. **Industrial PLC**: Siemens, Allen-Bradley, Mitsubishi
5. **Robots**: Serial, I2C, SPI, CAN, USB
6. **Sensors**: Temperature, Pressure, Motion, Light, Sound
7. **Actuators**: Motors, Servos, Relays, LEDs, Displays
8. **Communication**: UART, SPI, I2C, CAN, USB, Ethernet, WiFi, Bluetooth

## Quick Reference

### Hardware Abstraction
```
# Define hardware
board = Board("ESP32")
sensor = Sensor(board, pin=GPIO_0, type=TEMPERATURE)
motor = Motor(board, pins=[GPIO_1, GPIO_2], type=DC)
led = LED(board, pin=GPIO_3)
display = Display(board, type=OLED, width=128, height=64)
```

### Digital I/O
```
# Read digital pin
value = digital_read(pin=GPIO_0)

# Write digital pin
digital_write(pin=GPIO_1, value=HIGH)

# PWM output
pwm_write(pin=GPIO_2, duty=50, freq=1000)

# Analog input
voltage = analog_read(pin=ADC_0)
```

### Communication Protocols
```
# UART
uart = UART(board, baud=115200)
uart.write([0x01, 0x02, 0x03])
data = uart.read(10)

# I2C
i2c = I2C(board, sda=GPIO_4, scl=GPIO_5)
i2c.write_reg(addr=0x48, reg=0x00, data=[0x01])
data = i2c.read_reg(addr=0x48, reg=0x00, count=2)

# SPI
spi = SPI(board, mosi=GPIO_11, miso=GPIO_12, sck=GPIO_13)
spi.write([0x01, 0x02])
data = spi.transfer([0x01, 0x02, 0x03])

# CAN
can = CAN(board, speed=500000)
can.send(id=0x123, data=[0x01, 0x02, 0x03, 0x04])
msg = can.recv()
```

### Robot Control
```
# Define robot
robot = Robot(
    left_motor=Motor(pins=[GPIO_1, GPIO_2]),
    right_motor=Motor(pins=[GPIO_3, GPIO_4]),
    encoder_left=Encoder(pin_a=GPIO_5, pin_b=GPIO_6),
    encoder_right=Encoder(pin_a=GPIO_7, pin_b=GPIO_8)
)

# Basic movement
robot.forward(speed=100)
robot.backward(speed=100)
robot.left(speed=50)
robot.right(speed=50)
robot.stop()

# PID control
robot.pid(
    kp=1.0, ki=0.1, kd=0.01,
    target_speed=100,
    duration=5.0
)

# Path following
robot.follow_path([
    (100, 0),    # Forward 100cm
    (90, 1),     # Turn left 90 degrees
    (50, 0),     # Forward 50cm
    (-90, 1),    # Turn right 90 degrees
    (100, 0)     # Forward 100cm
])
```

### Sensor Integration
```
# Temperature sensor
temp_sensor = TemperatureSensor(board, pin=ADC_0)
temperature = temp_sensor.read()  # Returns temperature in Celsius

# Ultrasonic sensor
ultrasonic = UltrasonicSensor(board, trig=GPIO_9, echo=GPIO_10)
distance = ultrasonic.read()  # Returns distance in cm

# IMU (Inertial Measurement Unit)
imu = IMU(board, type=MPU6050, sda=GPIO_4, scl=GPIO_5)
accel = imu.read_accelerometer()
gyro = imu.read_gyroscope()
orientation = imu.read_orientation()

# GPS
gps = GPS(board, tx=GPIO_17, rx=GPIO_16)
position = gps.read_position()  # Returns (lat, lon, alt)
```

### Real-Time Control
```
# Timer interrupts
timer = Timer(board, frequency=1000)  # 1kHz
timer.callback(on_timer_tick)

def on_timer_tick():
    # This runs every 1ms
    sensor_value = analog_read(pin=ADC_0)
    if sensor_value > threshold:
        digital_write(pin=GPIO_0, value=HIGH)

# PWM control
servo = Servo(board, pin=GPIO_2, min_pulse=500, max_pulse=2500)
servo.set_angle(90)  # Set to 90 degrees

# Stepper motor
stepper = Stepper(
    board,
    pins=[GPIO_1, GPIO_2, GPIO_3, GPIO_4],
    steps_per_revolution=200
)
stepper.step(200)  # Rotate one full revolution
stepper.speed(1000)  # Set speed in RPM
```

### Communication
```
# WiFi
wifi = WiFi(board)
wifi.connect(ssid="MyNetwork", password="MyPassword")
server = TCPServer(port=80)
client = server.accept()
client.send("Hello!")
data = client.recv(1024)

# Bluetooth
ble = BLE(board)
ble.advertise("MyDevice")
client = ble.accept()
client.send("Hello!")
data = client.recv(1024)

# MQTT
mqtt = MQTT(board, broker="mqtt.example.com")
mqtt.subscribe("sensor/temperature")
mqtt.publish("sensor/led", "ON")
message = mqtt.recv()
```

### Safety Features
```
# Watchdog timer
watchdog = Watchdog(board, timeout=5.0)
watchdog.enable()

# Emergency stop
estop = EmergencyStop(board, pins=[GPIO_20, GPIO_21])
estop.callback(on_emergency_stop)

def on_emergency_stop():
    robot.stop()
    print("EMERGENCY STOP!")

# Current monitoring
current_sensor = CurrentSensor(board, pin=ADC_1)
if current_sensor.read() > MAX_CURRENT:
    robot.stop()
    throw OverCurrentError("Current exceeded limit")
```

## Running
```bash
# Interpret directly
python3 hardwarelang.py program.hw

# Compile to C (for microcontrollers)
python3 hardwarelang.py --compile-c program.hw

# Compile to Assembly (for bare metal)
python3 hardwarelang.py --compile-asm program.hw

# Upload to board
python3 hardwarelang.py --upload program.hw --board ESP32
```

## Difficulty Level
⭐⭐⭐ (3/10) - Easy to learn, powerful to master
