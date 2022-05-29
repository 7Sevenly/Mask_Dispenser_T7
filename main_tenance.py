import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

from system_lib import System


if __name__ == '__main__':
    # test servo motor
    system = System()
    system.open_door()
    time.sleep(2)
    system.stepper.act(1, 1000, "cw")
    system.display_stock_level()
    