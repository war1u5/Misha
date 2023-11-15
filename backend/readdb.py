from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('main_storage')
client.switch_user('warius', '12345678')

query = 'SELECT * FROM "kafka_consumer"'
result = client.query(query)

for point in result.get_points():
    print(point)
