import redis
import json


class RedisManager:
    def __init__(self, addr='localhost'):
        self.addr = addr
        parts = addr.split(':')
        host = parts[0]
        port = 6379
        if len(parts) > 1:
            port = int(parts[1])

        self.rconn = redis.StrictRedis(host=host, port=port)
        self.key = f"rm:{host}:{port}"

    def info(self, param="all"):
        return self.rconn.info(param)

    def add(self, now, value):
        self.rconn.zadd(self.key, {value: now})

    def get(self, minscore, maxscore):
        return [json.loads(x) for x in self.rconn.zrangebyscore(self.key, minscore, maxscore)]
