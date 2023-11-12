from influxdb import InfluxDBClient

# Create an InfluxDB client and connect to the database
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('main_storage')
client.switch_user('warius', '12345678')

# Query the database for all measurements
query = 'SELECT * FROM "kafka_consumer"'  # replace "your_measurement" with your actual measurement name
result = client.query(query)

# Print the result
for point in result.get_points():
    print(point)
