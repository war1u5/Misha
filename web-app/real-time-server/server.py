from flask import Flask, jsonify
from flask_cors import CORS
from influxdb import InfluxDBClient

app = Flask(__name__)
CORS(app)


@app.route('/api/gps-data')
def get_gps_data():
    client = InfluxDBClient(host='127.0.0.1',
                            port=8086,
                            username='warius',
                            password='12345678',
                            database='main_storage')

    #query = "SELECT Lat, Lng FROM kafka_consumer WHERE time > now() - 47900s"
    # query = "SELECT worker_id, Lat, Lng  FROM kafka_consumer WHERE Timestamp = 2857362"
    query = "SELECT worker_id, Lat, Lng, hello  FROM kafka_consumer WHERE time > now() - 1s"
    #query = "SELECT * FROM kafka_consumer WHERE time > now() - 47900s"
    result = client.query(query)
    data = list(result.get_points())
    print(data)
    client.close()

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
