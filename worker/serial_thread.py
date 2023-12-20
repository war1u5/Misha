from PyQt5.QtCore import QThread, pyqtSignal
import serial
import serial.serialutil
import json

from Misha.worker.kafka_producer import KafkaProducerWrapper
from worker_config import WORKER_ID, BAUD_RATE, ALL_DATA_KAFKA_TOPIC, KAFKA_SERVERS


class SerialThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, com_port):
        QThread.__init__(self)
        self.com_port = com_port
        self.kafka_producer_all = KafkaProducerWrapper(KAFKA_SERVERS, ALL_DATA_KAFKA_TOPIC)

    def run(self):
        global ser
        try:
            with serial.Serial(self.com_port, BAUD_RATE, timeout=1) as ser:
                while True:
                    try:
                        data = ser.readline().decode().strip()
                    except UnicodeDecodeError:
                        continue

                    if data:
                        message = {'worker_id': WORKER_ID, 'data': data}
                        self.signal.emit(message)

                        json_object = self.transform_message(message)

                        try:
                            self.kafka_producer_all.send_message(bytes(f'{json_object}', 'UTF-8'))
                        except Exception as kafka_error:
                            print(f"Error sending message to ALL_DATA_KAFKA_TOPIC: {kafka_error}")

        except serial.serialutil.SerialException as e:
            self.signal.emit(f"Error: {e}")
        finally:
            if ser.is_open:
                ser.close()

    def transform_message(self, message):
        data = message['data']
        split_message = data.split("'")[1].split(", ")
        json_message = {
            'worker_id': message['worker_id'],
            'hello': int(split_message[0].split(": ")[1]),
            'Valid': int(split_message[1].split(": ")[1]),
            'Lat': float(split_message[2].split(": ")[1]),
            'Lng': float(split_message[3].split(": ")[1]),
            'Satellites': int(split_message[4].split(": ")[1]),
            'Timestamp': int(split_message[5].split(": ")[1]),
            'Date': split_message[6].split(": ")[1],
            'Time': split_message[7].split(": ")[1],
            'RSSI': int(data.split()[-1])
        }
        return json.dumps(json_message)