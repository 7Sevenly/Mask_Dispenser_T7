import RPi.GPIO as GPIO
import pigpio
import time


class ServoMotor(object):
    
    def __init__(self, servo_pin):
        self.servo_pin = servo_pin
        
        # Pigpio generates a PWM signal from the built in hardware of the RasPi
        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.servo_pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(self.servo_pin, 50) # 50 Hz
        self.act(90)

    # To achieve rotation, to achieve door opening, or to rotate the belt
    def act(self, angle):
        # Ensure the given angle is within range
        if angle < 0:
            angle = 0
        if angle > 180:
            angle = 180
        
        # Determine the pulse width for the given angle
        pulse_width = ((angle * 100) / 9) + 500
        
        # Set the pulse width
        self.pwm.set_servo_pulsewidth(self.servo_pin, pulse_width)
        time.sleep(1)
        
        # Turn off the pwm to save power
        self.pwm.set_servo_pulsewidth(self.servo_pin, 0)
        
