# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template
from flask import request
from flask_cors import CORS, cross_origin

import time
import json

import atexit
import datetime
from optparse import OptionParser

from redis_manager import RedisManager
from redis_explainer import RedisExplainer
from store import Store
from poller import Poller


POLLING_INTERVAL = 5
PERIOD = 3600

store_mgr = Store(PERIOD/POLLING_INTERVAL)

parser = OptionParser()
parser.add_option("-a", "--addr", dest="addr", default="127.0.0.1",
                  help="hostaddr")
(options, args) = parser.parse_args()
print(options)
target_mgr = RedisManager(addr=options.addr)



app = Flask(__name__)
cors = CORS(app)


def get_current_timestamp():
    return int(datetime.datetime.utcnow().timestamp())


def parse_info(info: dict):
    return info


def collect_redis_info(mgr):
    info = mgr.info()
    return parse_info(info)


def sensor():
    value = collect_redis_info(target_mgr)
    value["time"] = get_current_timestamp()
    store_mgr.append(value)


poller = Poller.instance()
poller.add(sensor, POLLING_INTERVAL)


def make_histories(values):
    l = len(values)
    p0 = values[0]
    c = p0['total_commands_processed']
    tc = []
    labels = []
    rss = []
    for i in range(1, l):
        p = values[i]['total_commands_processed']
        label = datetime.datetime.fromtimestamp(values[i]['time']).strftime("%Y-%m-%d %H:%M:%S")
        rs = values[i]['used_memory_rss']/1024/1024/1024
        v = p - c
        c = p
        tc.append(v)
        labels.append(label)
        rss.append(rs)
        
    return {'commands': tc, 'labels': labels, 'rss': rss}


def Resp(code=0, message="ok"):
    return {'code': code, 'message': message}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/info', methods=['GET'])
def analysis():
    now = get_current_timestamp()
    values = store_mgr.get()
    
    resp = Resp()
    if values == None or len(values) == 0:
        return resp
    last = values[-1]
    results = make_histories(values)
    explainer = RedisExplainer(values)
    results['explains'] = explainer.explain()
    results['memory'] = {'rss': last['used_memory_rss_human'], 'used': last['used_memory_human'],
                         'peak': last['used_memory_peak_human']}

    resp['data'] = results
    return resp


@app.route('/api/v1/hello', methods=['GET'])
def hello():
    return redis_mgr.addr


if __name__ == '__main__':
    app.run('0.0.0.0')
