# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask import request

import redis
import time


app = Flask(__name__)
rconn = redis.StrictRedis()

SEED = 1592352000

def timestamp2str(ts):
    local_time = time.localtime(int(ts))
    return time.strftime("%Y-%m-%d %H:%M:%S", local_time)

@app.route('/api/v1/chart_data/<host>', methods=['GET'])
def getChartData(host):
    seed = int(request.args.get("seed"))
    min_seed = seed * 30 + SEED
    max_seed = (seed+30) * 30 + SEED
    key = "chart:" + host

    values = rconn.zrangebyscore(key, min_seed, max_seed) 
    labels = [timestamp2str(name.decode('utf-8').split(':')[0]) for name in values]
    data = [name.decode('utf-8').split(':')[1] for name in values]

    datasets = {
        "labels": labels,
        'data': data
    }

    result = {
        "code": 0,
        "message": "Ok",
        "datasets": datasets
    }

    resp = jsonify(result)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run()
