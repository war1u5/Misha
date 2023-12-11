from influxdb import InfluxDBClient

previous_hello = None


def get_gps_data():
    global previous_hello
    client = InfluxDBClient(host='127.0.0.1',
                            port=8086,
                            username='warius',
                            password='12345678',
                            database='main_storage')

    #query = "SELECT worker_id, Lat, Lng, hello FROM kafka_consumer ORDER BY time DESC LIMIT 1"
    query = "SELECT last(worker_id), last(Lat), last(Lng), last(hello) FROM kafka_consumer"
    #query = "SELECT worker_id, Lat, Lng, hello FROM kafka_consumer BY time DESC LIMIT 1"
    result = client.query(query)
    print(result)
    data = list(result.get_points())
    client.close()

    if not data:
        return None

    # if data and data[0]['hello'] == previous_hello:
    #     return None

    # if data:
    #     previous_hello = data[0]['hello']

    return data
