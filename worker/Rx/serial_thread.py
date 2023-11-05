from PyQt5.QtCore import QThread, pyqtSignal
import serial
import serial.serialutil
import logging

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
