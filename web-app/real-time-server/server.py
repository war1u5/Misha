from flask import Flask, jsonify
from flask_cors import CORS
from database import get_gps_data
from redis_publisher import publish_gps_data

app = Flask(__name__)
CORS(app)


@app.route('/api/gps-data')
def gps_data():
    data = get_gps_data()
    return jsonify(data)


@app.route('/api/gps-data-redis')
def gps_data_redis():
    data = get_gps_data()
    publish_gps_data(data)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
