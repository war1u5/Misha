import subprocess

kafka_zookeeper_file = "./kafka_zookeeper.yml"
telegraf_influxdb_file = "./telegraf_influxdb.yml"

subprocess.Popen(["docker-compose", "-f", telegraf_influxdb_file, "down"])
subprocess.Popen(["docker-compose", "-f", kafka_zookeeper_file, "down"])
