from kafka import KafkaProducer
import json


class KafkaProducerWrapper:
    def __int__(self, kafka_servers, kafka_topic):
        self.producer = KafkaProducer(bootstrap_servers=kafka_servers,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.topic = kafka_topic

    def send_message(self, message):
        self.producer.send(self.topic, message)
        self.producer.flush()
