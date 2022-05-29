import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


GPIO_Disp = 40

GPIO.setup(GPIO_Disp, GPIO.IN)


if __name__ == "__main__":
    #test GPIO input pin
    while(1):
        if GPIO.input(GPIO_Disp) == 1:
            print("OPEN")
            time.sleep(2)
        else:
            print("CLOSED")
            time.sleep(2)
    