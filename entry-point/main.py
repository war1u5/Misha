import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QComboBox, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
from serial.tools import list_ports
import serial

class SerialThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.serial_port = None

    def run(self):
        while True:
            if self.serial_port:
                line = self.serial_port.readline().decode('utf-8').strip()
                self.signal.emit(line)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.serial_thread = SerialThread()
        self.serial_thread.signal.connect(self.append_text)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Serial Reader')

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems([port.device for port in list_ports.comports()])

        self.button = QPushButton('Start', self)
        self.button.clicked.connect(self.start_reading)
        self.button.setStyleSheet("QPushButton { font-size: 20px; }")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.combo_box)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.text_edit)

        self.setLayout(self.layout)

    def start_reading(self):
        if not self.serial_thread.isRunning():
            port = str(self.combo_box.currentText())
            self.serial_thread.serial_port = serial.Serial(port, 115200)
            self.serial_thread.start()
            self.button.setText('Stop')
        else:
            self.serial_thread.serial_port.close()
            self.serial_thread.serial_port = None
            self.serial_thread.wait()
            self.button.setText('Start')

    def append_text(self, text):
        self.text_edit.append(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.showFullScreen()
    sys.exit(app.exec_())
