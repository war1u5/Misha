from flask import Flask, jsonify
from flask_cors import CORS
from database import get_gps_data

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/gps-data')
def gps_data():
    data = get_gps_data()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
