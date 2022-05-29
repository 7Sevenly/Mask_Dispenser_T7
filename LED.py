import RPi.GPIO as GPIO


class LED(object):
    """
    LED
    """
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    # turn on LED
    def turn_on(self):
        GPIO.output(self.pin, True)

    # turn off LED
    def turn_off(self):
        GPIO.output(self.pin, False)
