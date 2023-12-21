import serial
from confluent_kafka import Producer
import json

# Your existing code...
ser = serial.Serial()
ser.port = 'COM8'
ser.baudrate = 115200
ser.open()

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:29092',
    'security.protocol': 'PLAINTEXT',
    }

# Create Producer instance
p = Producer(**conf)

if ser.is_open:
    print("Successfully opened port", ser.port)
    try:
        while True:
            line = ser.readline().decode('ascii').strip()
            pairs = line.split(', ')
            data = {}
            for pair in pairs:
                key, value = pair.split(': ')
                data[key] = int(value)
            json_data = json.dumps(data)
            print(json_data)

            # Send the JSON data to the Kafka topic
            p.produce('all_data', json_data)
            p.flush()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()
else:
    print("Failed to open port", ser.port)
