import RPi.GPIO as GPIO
import time

# stepper
half_seq_ccw = [[1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1]]

half_seq_cw = [[0, 0, 0, 1],
               [0, 0, 1, 1],
               [0, 0, 1, 0],
               [0, 1, 1, 0],
               [0, 1, 0, 0],
               [1, 1, 0, 0],
               [1, 0, 0, 0],
               [1, 0, 0, 1]]

full_seq_ccw = [[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]

full_seq_cw = [[0, 0, 0, 1],
               [0, 0, 1, 0],
               [0, 1, 0, 0],
               [1, 0, 0, 0]]

time_scale = [1, 0.75, 0.5, 0.25,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class StepperMotor(object):
    """
    Stepper 

    """

    def __init__(self, motor_pins):
        # One motor corresponds to four pins, 
        # and the following are the corresponding pins of two motors. need to be entered when creating。
        # [3, 5, 7, 11], [16, 18, 22, 24]
        self.motor_pins = motor_pins
        
        # initial motor pins
        for outpin in self.motor_pins:
            GPIO.setup(outpin, GPIO.OUT)
            GPIO.output(outpin, 0)

    def act(self, motor_num, num_seq, direction):
        # The motor requires 8 cycles through a 64:1 gear ratio, to achieve a full cycle
        # Limiting the function to full cycles simplifies the code and is enough precision for the task at hand

        # Repeat loop for however many sequences requested, 512 sequences per revolution
        if direction == "cw":
            for i in range(num_seq):
                # Loop through 8 steps per sequence
                for half_step in range(8):
                    # Set all pins for the half step
                    for pin in range(4):
                        GPIO.output(self.motor_pins[pin + 4 * motor_num], half_seq_cw[half_step][pin])
                    # Sleep between steps to allow the motor time to react
                    time.sleep(time_scale[int((i / num_seq) * (len(time_scale) - 1))] * 0.004 + 0.001)
        elif direction == "ccw":
            for i in range(num_seq):
                # Loop through 8 steps per sequences
                for half_step in range(8):
                    # Set all pins for the half step
                    for pin in range(4):
                        GPIO.output(self.motor_pins[pin + 4 * motor_num], half_seq_ccw[half_step][pin])
                    # Sleep between steps to allow the motor time to react
                    time.sleep(time_scale[int((i / num_seq) * (len(time_scale) - 1))] * 0.004 + 0.001)
        else:
            print("Incorrect direction entered.")
        
        # Turn off pins
        for pin in range(4):
                        GPIO.output(self.motor_pins[pin + 4 * motor_num], 0)


    def act_all(self, num_seq, direction):
        # The motor requires 8 cycles through a 64:1 gear ratio, to achieve a full cycle
        # Limiting the function to full cycles simplifies the code and is enough precision for the task at hand

        # Repeat loop for however many sequences requested, 512 sequences per revolution
        if direction == "cw":
            for i in range(num_seq):
                # Loop through 8 steps per sequence
                for half_step in range(8):
                    # Set all pins for the half step
                    for pin in range(4):
                        GPIO.output(self.motor_pins[pin], half_seq_cw[half_step][pin])
                        GPIO.output(self.motor_pins[pin + 4], half_seq_ccw[half_step][pin])
                    # Sleep between steps to allow the motor time to react
                    time.sleep(time_scale[int((i / num_seq) * (len(time_scale) - 1))] * 0.004 + 0.001)
        elif direction == "ccw":
            for i in range(num_seq):
                # Loop through 8 steps per sequences
                for half_step in range(8):
                    # Set all pins for the half step
                    for pin in range(4):
                        GPIO.output(self.motor_pins[pin], half_seq_ccw[half_step][pin])
                        GPIO.output(self.motor_pins[pin + 4], half_seq_cw[half_step][pin])
                    # Sleep between steps to allow the motor time to react
                    time.sleep(time_scale[int((i / num_seq) * (len(time_scale) - 1))] * 0.004 + 0.001)
        else:
            print("Incorrect direction entered.")
        
        # Turn off pins
        for pin in range(4):
                        GPIO.output(self.motor_pins[pin], 0)
                        GPIO.output(self.motor_pins[pin + 4], 0)
