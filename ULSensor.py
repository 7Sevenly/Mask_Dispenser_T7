import RPi.GPIO as GPIO
import time

class ULSensor(object):
    """
    UL class
    """

    # Inititaise ultrasonic sensor pins - MM
    def __init__(self, ul_pins):
        self.trigger = ul_pins[0]
        self.echo = ul_pins[1]

        # Set trigger as output and echo as input - MM
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    # Function which returns the distance - MM
    def distance(self):
        # Set Trigger to HIGH
        GPIO.output(self.trigger, True)

        # set Trigger after 0.01ms to LOW creating a pulse - MM
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)

        StartTime = time.time()
        StopTime = time.time()

        # Save StartTime, start the timer - MM
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()

        # When the echo pin picks up a signal (echo equals 1) stop the timer - MM
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()

        # Determine the time of travel - MM
        TimeElapsed = StopTime - StartTime
        # Multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because we want the time from the object to the sensor - MM
        distance = (TimeElapsed * 34300) / 2

        return distance
