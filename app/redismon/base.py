# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redismon.config import Config

import redis

app = Flask(__name__)

config = Config("../redismon.ini")

db_config = config.get("db")
redis_config = config.get("redis")

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    db_config.get('user'),
    db_config.get('password'),
    db_config.get('host'),
    db_config.get('port'),
    db_config.get('database'))

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'flasknotewithsqlalchemy'

db = SQLAlchemy(app)
redis_conn = redis.StrictRedis(host=redis_config.get("host"),
                          port=int(redis_config.get("port")))
