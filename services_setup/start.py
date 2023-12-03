import subprocess
import time

kafka_zookeeper_file = "kafka_zookeeper.yml"
telegraf_influxdb_grafana_file = "telegraf_influxdb_grafana.yml"
postgres_file = "postgres.yml"

subprocess.Popen(["docker-compose", "-f", kafka_zookeeper_file, "up", "-d"])

time.sleep(7)

subprocess.Popen(["docker-compose", "-f", telegraf_influxdb_grafana_file, "up", "-d"])

time.sleep(5)

subprocess.Popen(["docker-compose", "-f", postgres_file, "up", "-d"])
