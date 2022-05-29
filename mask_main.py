from system_lib import *
from PyQt5.QtCore import pyqtSignal, QThread, QMutex


class MaskSystem(QThread):
    # Send signal to the main GUI window - MM
    msg_signal = pyqtSignal(str)
    mask_dispense_signal = pyqtSignal(int)
    # Inherit system MaskSystem class - MM
    def __init__(self):
        super(MaskSystem, self).__init__()
        self.system = System()

    # Handle dispensing logic - MM
    def run(self):
        while(True):
            # Check if there is mask in stock and report empty
            if self.system.is_mask_tray_empty():
                self.report_empty()
            else:
                # Update the stock level LED
                self.system.display_stock_level()

            # Check if the path is clear
            # If mask is uncollected in waiting position, report fault - MM
            if self.system.is_mask_in_waiting_position():
                self.report_fault()
            else:
                # Is ready to dispense - MM
                self.system.close_door()
                self.system.led_ready.turn_on()
                # Waiting for user to issue a mask request - MM
                self.system.wait_request()

            # A user has requested a mask
            # Activate dispensing LED and actuate stepper counter clockwise - MM
            self.system.reset_report_led()
            self.system.led_dispensing.turn_on()
            self.system.stepper.act_all(400, "ccw")  # Partially slide mask out of stack - MM

            # Open the door and further dispense the mask
            # Collection position
            self.system.open_door()

            self.system.stepper.act(1, 900, "cw")

            # Check if the mask didn't get to the waiting position, meaning it jammed in the belt - MM
            if not self.system.is_mask_in_waiting_position():
                self.report_fault()

            # Wait 2.5 seconds for the user to collect
            time.sleep(2.5)

            # If no user collects the mask , fully eject the mask by running the rollers
            # with 2 full rotations - MM
            if self.system.is_mask_in_waiting_position():
                self.system.stepper.act(1, 1024, "cw")
                self.system.servo.act(80)
                self.system.open_door()
                self.system.servo.act(80)
                self.system.open_door()

            # If mask is still in waiting position uncollected, meaning a jam, report fault - MM
            if self.system.is_mask_in_waiting_position():
                self.report_fault()

            # Finish up by closing the door and turning off dispensing LED - MM
            self.system.close_door()
            self.system.led_dispensing.turn_off()
            self.system.stack_count -= 1
            # Display mask dispensed message on GUI - MM
            self.send_mask_dispensed()
            self.send_msg("Dispensed mask")
            self.system.reset_report_led()
            
    # Turn on fault LED and trap the system in a loop
    def report_fault(self):
        self.system.reset_report_led()
        self.system.led_fault.turn_on()
        self.send_msg('There was a FAULT.')
        while (1):
            time.sleep(2)
    
    
    # Trap the system in a loop and flash the 0% LED when the empty light gate is true
    def report_empty(self):
        self.system.reset_stock_led()
        # Report empty message on GUI - MM
        self.send_msg('The stock is EMPTY.')
        # Have '0% LED' flashing in 1 second periods - MM
        while (1):
            self.system.led_0P.turn_on()
            time.sleep(1)
            self.system.led_0P.turn_off()
            time.sleep(1)

    # Set the set count number  - MM
    def set_stack_count(self, num):
        self.system.stack_count = num
    
    # Send signal to GUI that a mask has been dispensed and to decrease the mask count
    def send_mask_dispensed(self):
        self.mask_dispense_signal.emit(self.system.stack_count)

    # Send message to the GUI
    def send_msg(self, string):
        self.msg_signal.emit(string)
