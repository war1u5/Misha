import serial
from confluent_kafka import Producer
import json

worker_id = 1
ser = serial.Serial()
ser.port = 'COM5'
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
            try:
                line = ser.readline().decode('ascii').strip()
                pairs = line.split(', ')
                data = {}
                for pair in pairs:
                    try:
                        key, value = pair.split(': ')
                        data[key] = int(value)
                    except ValueError:
                        print("Data received does not contain expected delimiter, continuing...")
                        continue
                data['worker_id'] = worker_id
                # json_data = json.dumps(data)
                # print(json_data)

                p.produce('all_data', json.dumps(data))
                p.flush()
            except UnicodeDecodeError:
                print("Non-ASCII data received, continuing...")
                continue
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()
else:
    print("Failed to open port", ser.port)
