from PyQt5.QtCore import QThread, pyqtSignal
import serial
import serial.serialutil
import logging

from kafka_producer import KafkaProducerWrapper
from worker_config import WORKER_ID, BAUD_RATE, GPS_DATA_KAFKA_TOPIC, KAFKA_SERVERS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SerialThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, com_port):
        QThread.__init__(self)
        self.com_port = com_port
        self.kafka_producer = KafkaProducerWrapper(KAFKA_SERVERS, GPS_DATA_KAFKA_TOPIC)

    def run(self):
        global ser
        try:
            ser = serial.Serial(self.com_port, BAUD_RATE, timeout=1)  # Set a timeout value in seconds
            logger.info(f"Connected to {self.com_port} at {BAUD_RATE} baud")

            while True:
                data = ser.readline().decode().strip()
                if data:  # Check if data is not empty
                    message = {'worker_id': WORKER_ID, 'data': data}
                    self.signal.emit(message)
                    logger.info(f"Sent data: {message}")
                    self.kafka_producer.send_message(message)

        except serial.serialutil.SerialException as e:
            self.signal.emit(f"Error: {e}")
            logger.error(f"Error: {e}")
        finally:
            if ser.is_open:
                ser.close()
                logger.info("Serial port closed")
