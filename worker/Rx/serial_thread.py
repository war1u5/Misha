from PyQt5.QtCore import QThread, pyqtSignal
import serial
import serial.serialutil
import json

from kafka_producer import KafkaProducerWrapper
from worker_config import WORKER_ID, BAUD_RATE, GPS_DATA_KAFKA_TOPIC, KAFKA_SERVERS


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

            while True:
                data = ser.readline().decode().strip()
                if data:  # if data is not empty
                    message = {'worker_id': WORKER_ID, 'data': data}
                    print(message)
                    # message = self.transform_message(data)
                    self.signal.emit(message)
                    # self.kafka_producer.send_message(json.dumps(message))

        except serial.serialutil.SerialException as e:
            self.signal.emit(f"Error: {e}")
        finally:
            if ser.is_open:
                ser.close()

    def transform_message(self, message):
        split_message = message.split(", ")
        json_message = {
            'worker_id': WORKER_ID,
            'hello': split_message[0].split(" ")[1],
            'Valid GPS data': int(split_message[1].split(": ")[1]),
            'Lat': float(split_message[2].split(": ")[1]),
            'Lng': float(split_message[3].split(": ")[1]),
            'Satellites': int(split_message[4].split(": ")[1]),
            'Timestamp': int(split_message[5].split(": ")[1]),
            'Date': split_message[6].split(": ")[1],
            'Time': split_message[7].split(": ")[1]
        }
        return json_message
