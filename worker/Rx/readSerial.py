import serial
import serial.serialutil
# from kafka import KafkaProducer
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COM_PORT = 'COM8'
BAUD_RATE = 115200
WORKER_ID = 'worker_1'  # Replace with your worker ID

# producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)  # Set a timeout value in seconds
    logger.info(f"Connected to {COM_PORT} at {BAUD_RATE} baud")

    while True:
        data = ser.readline().decode().strip()
        if data:  # Check if data is not empty
            message = {'worker_id': WORKER_ID, 'data': data}
            # print(message)
            # producer.send('gps_data', message)
            logger.info(f"Sent data: {message}")

except serial.serialutil.SerialTimeoutException:
    logger.error("Serial communication timed out.")
except serial.SerialException as e:
    logger.error(f"Error: {e}")
finally:
    if ser.is_open:
        ser.close()
        logger.info("Serial port closed")
