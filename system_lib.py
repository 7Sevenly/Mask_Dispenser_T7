import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

from Lib.Button import Button
from Lib.IRSensor import IRSensor
from Lib.LED import LED
from Lib.ServoMotor import ServoMotor
from Lib.StepperMotor import StepperMotor
from Lib.ULSensor import ULSensor
from const import *

"""
A class which declares and defines the multiple components of the system,
and defines functions to communicate and control them.
"""
class System(object):
    
    # Initialise
    def __init__(self):
        # Begin with a stack count of 50 masks
        self.stack_count = 50

        ### Initialise Components ###
        # IR sensors
        self.IR_sensor_Empty = IRSensor(IR_EMPTY)
        self.IR_sensor_25P = IRSensor(IR_25P)
        self.IR_sensor_50P = IRSensor(IR_50P)
        self.IR_sensor_75P = IRSensor(IR_75P)
        self.IR_sensor_Collect = IRSensor(IR_COLLECT)

        # Ultrasonic sensor
        self.ul_sensor = ULSensor(UL_SON)

        # Stepper motors
        self.stepper = StepperMotor(STEPPER)

        # Servo motor
        self.servo = ServoMotor(SERVO)

        # Reset Button
        self.reset_button = Button(BUTTON)

        # Status LED Display
        self.led_ready = LED(LED_READY)
        self.led_user = LED(LED_USER)
        self.led_dispensing = LED(LED_DISPENSING)
        self.led_fault = LED(LED_FAULT)
        
        # Stock Level LED Display
        self.led_100P = LED(LED_100P)
        self.led_75P = LED(LED_75P)
        self.led_50P = LED(LED_50P)
        self.led_25P = LED(LED_25P)
        self.led_0P = LED(LED_EMPTY)
        
        # Turn off all LEDs initially
        self.reset_stock_led()
        self.reset_report_led()

    # Reset the system
    def reset(self):
        self.reset_stock_led()
        self.reset_report_led()
        self.close_door()

    # Reset the stock level display
    def reset_stock_led(self):
        # Turn off all LEDs
        self.led_0P.turn_off()
        self.led_25P.turn_off()
        self.led_50P.turn_off()
        self.led_75P.turn_off()
        self.led_100P.turn_off()

    # Reset the status display
    def reset_report_led(self):
        # Turn off all LEDS
        self.led_dispensing.turn_off()
        self.led_fault.turn_off()
        self.led_ready.turn_off()
        self.led_user.turn_off()

    # Determines the stock level using the light gates and update the LED display - MM
    def display_stock_level(self):
        # Reset the stock level LED display
        self.reset_stock_led()
        
        # Investigate IR sensors from the bottom to top
        # turn on the corresponding LED for the 0-25, 25-50, 50-75 IR sensor

        # 0 - 25%
        # If the 25% light gate is open (detecting IR light), have the 0% and 25% LEDs on - MM
        if self.IR_sensor_25P.read_data() == OPEN:
            self.led_0P.turn_on()
            self.led_25P.turn_on()
            return
        # 25-50%
        # If the 50% light gate is open (etecting IR light), have the 0%, 25%, and 50% LEDs on - MM
        elif self.IR_sensor_50P.read_data() == OPEN:
            self.led_0P.turn_on()
            self.led_25P.turn_on()
            self.led_50P.turn_on()
            return
        # 50-75%
        # If the 75% light gate is open (detecting IR light), have 0%, 25%, 50%, and 75% LEDs on - MM
        elif self.IR_sensor_75P.read_data() == OPEN:
            self.led_0P.turn_on()
            self.led_25P.turn_on()
            self.led_50P.turn_on()
            self.led_75P.turn_on()
            return
        # 100%
        # If the 100% light gate is closed (not detecting IR light), have all the stack level LEDs on - MM
        else:
            self.led_0P.turn_on()
            self.led_25P.turn_on()
            self.led_50P.turn_on()
            self.led_75P.turn_on()
            self.led_100P.turn_on()
            return


    # Check if the mask tray is empty - MM
    # If the empty light gate is open (detecting IR light) then the dispenser is empty - MM
    def is_mask_tray_empty(self):
        if self.IR_sensor_Empty.read_data() == OPEN:
            return True
        else:
            return False
    
    # Check if the user is requesting mask (user needs to present hand for >= 1 sec within 40cm of sensor)
    # - MM
    def is_mask_requested(self):
        # Check whether an object is within 40cm of the ultrasonic sensor
        if self.ul_sensor.distance() < 40:
            # Turn on the User LED and wait 1 second - MM
            self.led_user.turn_on()
            time.sleep(1.0)
        else:
            # Ensure User LED is off and return false
            self.led_user.turn_off()
            return False
        
        # After the 1 second, check for object again to ensure no accidental trigger
        if self.ul_sensor.distance() < 40:
            # Turn off the User LED and return True
            self.led_user.turn_off()
            return True
        else:
            # False trigger
            self.led_user.turn_off()
            return False

    # Check if the mask is in the waiting position - MM
    # If the dispensing light-gate is blocked (mask is blocking IR light) then a mask is
    # in the waiting position - MM
    def is_mask_in_waiting_position(self):
        if self.IR_sensor_Collect.read_data() == BLOCKED:
            return True
        else:
            return False
    
    # Wait_request if mask is not being requested
    def wait_request(self):
        while not self.is_mask_requested():
            # Poll every 1 seconds to check whether a client sends a mask request - MM
            time.sleep(0.1)

    # Open door
    def open_door(self):
        self.servo.act(60)

    # Close door
    def close_door(self):
        self.servo.act(165)
