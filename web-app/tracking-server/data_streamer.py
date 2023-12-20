from fastapi import FastAPI, WebSocket

from confluent_kafka import Consumer, KafkaException
import asyncio

app = FastAPI()


def create_consumer():
    # Define the consumer configuration
    conf = {
        'bootstrap.servers': 'kafka:9092',  # Broker address
        'group.id': 'all_data',  # Consumer group
        'auto.offset.reset': 'oldest',  # Start reading from the beginning if no offset is stored
    }

    # Create the consumer
    consumer = Consumer(conf)

    # Subscribe to the topic
    consumer.subscribe(['all_data'])

    return consumer


def process_data(message):
    # Add your data processing logic here
    print(f"Received message: {message.key()} -> {message.value()}")
    return message.value().decode('utf-8')


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    consumer = create_consumer()
    await websocket.accept()
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Process the data and send it to the frontend via the WebSocket
            data = process_data(msg)
            await websocket.send_text(data)
