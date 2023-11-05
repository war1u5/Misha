from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
from serial.tools import list_ports
import serial
import serial.serialutil
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WORKER_ID = 'worker_1'
BAUD_RATE = 115200  # Set baud rate to 115200 by default

class SerialThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, com_port):
        QThread.__init__(self)
        self.com_port = com_port

    def run(self):
        try:
            ser = serial.Serial(self.com_port, BAUD_RATE, timeout=1)  # Set a timeout value in seconds
            logger.info(f"Connected to {self.com_port} at {BAUD_RATE} baud")

            while True:
                data = ser.readline().decode().strip()
                if data:  # Check if data is not empty
                    message = {'worker_id': WORKER_ID, 'data': data}
                    self.signal.emit(f"Sent data: {message}")
                    logger.info(f"Sent data: {message}")

        except serial.serialutil.SerialException as e:
            self.signal.emit(f"Error: {e}")
            logger.error(f"Error: {e}")
        finally:
            if ser.is_open:
                ser.close()
                logger.info("Serial port closed")


class SerialParametersApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serial Parameters")
        self.resize(600, 500)

        self.layout = QVBoxLayout()

        self.com_label = QLabel("COM Port:")
        self.layout.addWidget(self.com_label)

        self.com_dropdown = QComboBox()
        com_ports = [port.device for port in list_ports.comports()]
        self.com_dropdown.addItems(com_ports)
        self.layout.addWidget(self.com_dropdown)

        self.submit_button = QPushButton("Start reception")
        self.submit_button.clicked.connect(self.set_serial_parameters)
        self.layout.addWidget(self.submit_button)

        self.clear_button = QPushButton("Clear Screen")
        self.clear_button.clicked.connect(self.clear_output_text)
        self.layout.addWidget(self.clear_button)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.setLayout(self.layout)

    def set_serial_parameters(self):
        com_port = self.com_dropdown.currentText()
        self.start_serial_communication(com_port)

    def start_serial_communication(self, com_port):
        self.serial_thread = SerialThread(com_port)
        self.serial_thread.signal.connect(self.update_output_text)
        self.serial_thread.start()

    def update_output_text(self, text):
        self.output_text.append(text)

    def clear_output_text(self):
        self.output_text.clear()


app = QApplication(sys.argv)

window = SerialParametersApp()
window.show()

sys.exit(app.exec_())
