from kafka import KafkaConsumer
import json


class KafkaConsumerWrapper:
    def __init__(self, kafka_servers, kafka_topic):
        self.consumer = KafkaConsumer(kafka_topic,
                                      bootstrap_servers=kafka_servers,
                                      value_deserializer=lambda v: json.loads(v.decode('utf-8')))

    def start_consuming(self):
        for message in self.consumer:
            print(message.value)
