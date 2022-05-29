import RPi.GPIO as GPIO


class IRSensor(object):
    """
    IR class
    """

    # Initialise input pins
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    # Red IR GPIO
    def read_data(self):
        return GPIO.input(self.pin)
