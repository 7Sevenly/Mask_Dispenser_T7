##### Constant Varaibles #####

# IR Light Gate States
BLOCKED = 0
OPEN = 1

### Pin Allocation ###
# LED Display Pins
LED_FAULT = 31
LED_READY = 33
LED_USER = 35
LED_DISPENSING = 37

LED_EMPTY = 23
LED_25P = 21
LED_50P = 19
LED_75P = 15
LED_100P = 13

# IR Sensor Pins
IR_75P = 40
IR_50P = 38
IR_25P = 36
IR_EMPTY = 32
IR_COLLECT = 26

# Ultrasonic Sensor Pins
UL_SON = [8, 10]

# Stepper Pins
STEPPER = [3, 5, 7, 11, 16, 18, 22, 24]

# Servo Pin
SERVO = 18  # The board pin is 12, however the servo motor is controlled by pigpio, which uses GPIO pin allocation

# Reset Button Pin
BUTTON = 29



