from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from serial.tools import list_ports
import serial
import serial.serialutil
import logging
import sys
import pyqtgraph as pg
import numpy as np

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
        global ser
        try:
            ser = serial.Serial(self.com_port, BAUD_RATE, timeout=1)  # Set a timeout value in seconds
            logger.info(f"Connected to {self.com_port} at {BAUD_RATE} baud")

            while True:
                data = ser.readline().decode().strip()
                if data:  # Check if data is not empty
                    message = {'worker_id': WORKER_ID, 'data': data}
                    self.signal.emit(message)  # Emit the whole message
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

        self.serial_thread = None
        self.setWindowTitle("Worker interface")
        self.showMaximized()

        self.layout = QVBoxLayout()

        self.left_layout = QVBoxLayout()
        self.layout.addLayout(self.left_layout)

        self.com_label = QLabel("COM Port:")
        self.com_label.setStyleSheet("font-size: 20px;")
        self.left_layout.addWidget(self.com_label)

        self.com_dropdown = QComboBox()
        com_ports = [port.device for port in list_ports.comports()]
        self.com_dropdown.addItems(com_ports)
        self.left_layout.addWidget(self.com_dropdown)

        self.submit_button = QPushButton("Start reception")
        self.submit_button.clicked.connect(self.set_serial_parameters)
        self.left_layout.addWidget(self.submit_button)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.left_layout.addWidget(self.output_text)

        self.clear_button = QPushButton("Clear Screen")
        self.clear_button.clicked.connect(self.clear_output_text)
        self.left_layout.addWidget(self.clear_button)

        self.graph = pg.PlotWidget()
        self.graph.setLabel('left', 'RSSI')  # Label the y-axis as "RSSI"
        self.graph.setLabel('bottom', 'Time')  # Label the x-axis as "Time"
        self.layout.addWidget(self.graph)

        self.rssi_data = np.array([])

        self.setLayout(self.layout)

    def set_serial_parameters(self):
        com_port = self.com_dropdown.currentText()
        self.start_serial_communication(com_port)

    def start_serial_communication(self, com_port):
        self.serial_thread = SerialThread(com_port)
        self.serial_thread.signal.connect(self.update_output_text)
        self.serial_thread.start()

    def update_output_text(self, message):
        if isinstance(message, str):  # If the message is a string, it's an error message
            self.output_text.append(message)
        else:  # If the message is a dict, it's a data packet
            self.output_text.append(message['data'])
            rssi = self.extract_rssi(message['data'])  # Extract the RSSI value from the data packet
            self.update_graph(rssi)

    def clear_output_text(self):
        self.output_text.clear()

    def extract_rssi(self, data):
        # Split the data packet into a list of strings
        data_list = data.split()

        # The RSSI value is the last element in the list
        rssi_str = data_list[-1]

        # Convert the RSSI value to an integer
        rssi = int(rssi_str)

        return rssi

    def update_graph(self, rssi):
        self.rssi_data = np.append(self.rssi_data, rssi)
        self.graph.plot(self.rssi_data, pen='y')


app = QApplication(sys.argv)
app.setStyleSheet("""
    QWidget { 
        background-color: #202020; 
        color: #ffffff; 
    } 
    QPushButton, QComboBox { 
        background-color: #0066CC; 
        font-size: 20px;
    }
    QTextEdit {
        background-color: #000000;
        color: #00FF00;
        font-size: 20px;
    }
""")  # Set background color to black, text color to white, and button/dropdown color to green
app.setWindowIcon(QIcon('../../utils/images/workerAppLogo.png'))


window = SerialParametersApp()
window.show()

sys.exit(app.exec_())
