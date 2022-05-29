import sys

import time
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QMutex
from PyQt5.QtWidgets import QApplication, QMainWindow

from MaskUi import Ui_MainWindow
from mask_main import MaskSystem

mutex = QMutex()


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    main window
    """

    # Initialize 
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #Initialise mask count to zero - MM
        self.mask_num = 0
        
        # connection slot function
        # Check for clear status button - MM
        self.Clear_status_btn.clicked.connect(self.clear_feedback_bro)

        self.Demo_btn.clicked.connect(self.start_mask_mech)
        self.Stop_Demo_btn.clicked.connect(self.stop_mask_mech)

        # Menu button clicks - MM
        self.actionRefill_mask.triggered.connect(lambda: self.set_mask_num(50))
        self.actionEmpty_mask.triggered.connect(lambda: self.set_mask_num(0))
        self.actionRemove_1mask.triggered.connect(lambda: self.mask_num_decrease_by(1))
        self.actionRemove_10mask.triggered.connect(lambda: self.mask_num_decrease_by(10))
        self.actionRemove_50mask.triggered.connect(lambda: self.mask_num_decrease_by(50))
        self.actionAdd_1mask.triggered.connect(lambda: self.mask_num_increase_by(1))
        self.actionAdd_10mask.triggered.connect(lambda: self.mask_num_increase_by(10))
        self.actionAdd_50mask.triggered.connect(lambda: self.mask_num_increase_by(50))

    # Each call, reduce the corresponding number of masks
    # num_decrease is the amount to be reduced
    def mask_num_decrease_by(self, num):
        mask_number = int(self.Mask_number_bro.toPlainText())
        mask_number -= num
        self.mask_num = mask_number
        self.set_mask_num(mask_number)


    # Add the number of masks in GUI
    def mask_num_increase_by(self, num):
        mask_number = int(self.Mask_number_bro.toPlainText())
        mask_number += num
        self.mask_num = mask_number
        self.set_mask_num(mask_number)

    # Display message as string in GUI - MM
    def display_msg(self, string):
        self.Feedback_bro.append(string)

    # Set the number of masks in the dispenser - MM
    def set_mask_num(self, num):
        # Display number of masks - MM
        display = str(num)
        self.Mask_number_bro.setText(display)
        self.Mask_number_bro.setAlignment(Qt.AlignCenter)

    # Clear status message button in GUI - MM
    def clear_feedback_bro(self):
        self.Feedback_bro.clear()

    # Main thread - MM
    def start_mask_mech(self):
        self.mask_system = MaskSystem()
        self.mask_system.set_stack_count(self.mask_num)
        # Display msg_signal in display_msg function as string - MM
        self.mask_system.msg_signal[str].connect(self.display_msg)
        self.mask_system.mask_dispense_signal[int].connect(self.set_mask_num)
        self.mask_system.start()

    # End main thread - MM
    def stop_mask_mech(self):
        if hasattr(self, "mask_system"):
            mutex.lock()
            self.mask_system.requestInterruption()
            # Quit and end the thread - MM
            self.mask_system.quit()
            mutex.unlock()
            del self.mask_system
   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
