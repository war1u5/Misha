from confluent_kafka import Consumer, KafkaError

# Kafka configuration
conf = {'bootstrap.servers': 'localhost:9092', 'group.id': 'your_group_id', 'auto.offset.reset': 'earliest'}

# Create Consumer instance
c = Consumer(conf)

# Subscribe to the topic
c.subscribe(['test_topic'])

try:
    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Print the message
        print('Received message: {}'.format(msg.value().decode('utf-8')))

except KeyboardInterrupt:
    print('Stopped.')

finally:
    # Close down consumer to commit final offsets.
    c.close()
