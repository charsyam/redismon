# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask import request

from redismon.base import app, db, config
from redismon.redismon_manager import RedisMonManager

import redis
import time


SEED = 1592352000

manager = RedisMonManager(db)

redis_config = config.get("redis")
rconn = redis.StrictRedis(host=redis_config.get("host"), port=int(redis_config.get("port")))

def response_object(code, message, data=None):
    resp = {"code": code, "message": message}
    if data != None:
        resp.update(data)
    return resp


def response_objects(code, message, data):
    data_json = list(map(lambda x: x.to_dict(), data))
    resp = {"code": code, "message": message, "data": data_json}
    return resp

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


@app.route('/api/v1/groups', methods=['POST'])
def create_groups():
    param = request.get_json()
    name = param["name"]
    seed = param["seed"]
    group = manager.create_monitoring_group(name, seed)
    return response_object(0, "Ok", group.to_dict())


@app.route('/api/v1/groups', methods=['GET'])
def list_groups():
    groups = manager.list_monitoring_groups()
    return response_objects(0, "Ok", groups)


@app.route('/api/v1/groups/<group_id>', methods=['DELETE'])
def delete_groups(group_id):
    groups = manager.delete_monitoring_group(group_id)
    return response_object(0, "Ok")
     

if __name__ == '__main__':
    app_config = config.get("app")
    app.run(host=app_config.get("host"), port=int(app_config.get("port")))
