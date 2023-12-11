import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)


def publish_gps_data(data):
    gps_data_json = json.dumps(data)
    r.publish('gps-updates', gps_data_json)
