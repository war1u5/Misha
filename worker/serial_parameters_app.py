from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QPushButton, QLabel, QTextEdit
# from PyQt5.QtGui import QIcon
from serial.tools import list_ports
from serial_thread import SerialThread
import numpy as np
import pyqtgraph as pg
import subprocess


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

        if not com_ports:
            self.check_ports()
            self.submit_button.setEnabled(False)
            self.clear_button.setEnabled(False)
        else:
            self.submit_button.setEnabled(True)
            self.clear_button.setEnabled(True)
            subprocess.Popen(["python", "../services_setup/start.py"])

    def check_ports(self):
        self.output_text.append("<font color='red'>Error: No COM ports available.</font>")

    def set_serial_parameters(self):
        com_port = self.com_dropdown.currentText()
        self.start_serial_communication(com_port)

    def start_serial_communication(self, com_port):
        self.serial_thread = SerialThread(com_port)
        self.serial_thread.signal.connect(self.update_output_text)
        self.serial_thread.start()

    def update_output_text(self, message):
        if isinstance(message, str) and message.startswith("Error:"):
            self.output_text.append("<font color='red'>" + message + "</font>")
        elif isinstance(message, dict):
            self.output_text.append(message['data'])
            rssi = self.extract_rssi(message['data'])
            self.update_graph(rssi)
        else:
            self.output_text.append(message)

    def clear_output_text(self):
        self.output_text.clear()

    def extract_rssi(self, data):
        data_list = data.split()
        rssi_str = data_list[-1]
        rssi = int(rssi_str)
        return rssi

    def update_graph(self, rssi):
        self.rssi_data = np.append(self.rssi_data, rssi)
        self.graph.plot(self.rssi_data, pen='y')
