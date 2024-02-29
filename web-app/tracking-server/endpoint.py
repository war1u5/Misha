import asyncio
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from confluent_kafka import Consumer
import json
import threading

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.is_tracking = False

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_data(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)


manager = ConnectionManager()

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest',
}

c = Consumer(conf)
c.subscribe(['all_data'])


def start_kafka_consumer():
    while manager.is_tracking:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        # data = msg.value().decode('utf-8')
        asyncio.run(manager.send_data(
                                msg.value().decode('utf-8')))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            action = json.loads(data).get('action')
            if action == 'start':
                manager.is_tracking = True
                threading.Thread(target=start_kafka_consumer, daemon=True).start()
            elif action == 'stop':
                manager.is_tracking = False
    except WebSocketDisconnect:
        manager.disconnect(websocket)
