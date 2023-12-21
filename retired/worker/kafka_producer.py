from kafka import KafkaProducer


class KafkaProducerWrapper:
    def __init__(self, kafka_servers, kafka_topic):
        self.producer = KafkaProducer(bootstrap_servers=kafka_servers)
        self.topic = kafka_topic

    def send_message(self, message):
        self.producer.send(self.topic, value=message)
        self.producer.flush()
