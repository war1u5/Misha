import subprocess

kafka_zookeeper_file = "kafka_zookeeper.yml"
telegraf_influxdb_grafana_file = "telegraf_influxdb_grafana.yml"
postgres_file = "postgres.yml"

subprocess.Popen(["docker-compose", "-f", telegraf_influxdb_grafana_file, "down"])
subprocess.Popen(["docker-compose", "-f", kafka_zookeeper_file, "down"])
subprocess.Popen(["docker-compose", "-f", postgres_file, "down"])
