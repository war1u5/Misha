from confluent_kafka import Consumer, KafkaException
import asyncio


def create_consumer():
    # Define the consumer configuration
    conf = {
        'bootstrap.servers': 'localhost:29092',  # Broker address
        'group.id': 'all_data',  # Consumer group
        'auto.offset.reset': 'earliest',  # Start reading from the beginning if no offset is stored
    }

    # Create the consumer
    consumer = Consumer(conf)

    # Subscribe to the topic
    consumer.subscribe(['all_data'])

    return consumer

