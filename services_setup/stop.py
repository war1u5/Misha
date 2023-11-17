import subprocess

kafka_zookeeper_file = "../services_setup/kafka_zookeeper.yml"
telegraf_influxdb_file = "../services_setup/telegraf_influxdb.yml"

subprocess.Popen(["docker-compose", "-f", telegraf_influxdb_file, "down"])
subprocess.Popen(["docker-compose", "-f", kafka_zookeeper_file, "down"])
