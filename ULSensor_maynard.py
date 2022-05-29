# ultrasonic2

import RPi.GPIO as GPIO
import time
from const import *


# set GPIO direction (IN / OUT)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()
        # print("lol")

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


# if __name__ == 'main':
#     try:
#         while True:
#             dist = distance()
#             print("Measured Distance = %.1f cm" % dist)
#             time.sleep(1)
#
#             if (dist < 40):
#                 GPIO.output(GPIO_LED, True)
#                 print("User Detected")
#             else:
#                 GPIO.output(GPIO_LED, False)
#
#         # Reset by pressing CTRL + C
#     except KeyboardInterrupt:
#         print("Measurement stopped by User")
#         GPIO.cleanup()

