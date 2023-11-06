from consumer_config import KAFKA_SERVERS, GPS_DATA_KAFKA_TOPIC
from kafka_consumer import KafkaConsumerWrapper


def main():
    kafka_consumer = KafkaConsumerWrapper(KAFKA_SERVERS, GPS_DATA_KAFKA_TOPIC)
    kafka_consumer.start_consuming()


if __name__ == "__main__":
    main()
