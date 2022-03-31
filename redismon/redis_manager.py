import redis
import json


def get_string_key_size(conn, key):
    return len(conn.get("key"))

def get_hash_key_size(conn, key):
    return len(conn.hgetall(key))

def get_set_key_size(conn, key):
    return len(conn.smembers(key))

def dump(conn, key):
    data = conn.dump(key)
    l = len(data) if data else 0
    return l

def get_all_items_size(conn, limit):
    all = {}

    for key in conn.scan_iter(count=100):
        dtype = conn.type(key)
        size = dump(conn, key)

        if size >= limit:
            if size not in all:
                all[size] = []

            all[size].append({"type": dtype.decode(), "key": key.decode()})

    return all


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
        self.host = f"{host}:{port}"

    def get_host(self):
        return self.host

    def info(self, param="all"):
        return self.rconn.info(param)

    def get_config(self, key):
        return self.rconn.config_get(key)

    def check_size(self, limit = 1024768):
        all = get_all_items_size(self.rconn, limit)
        return all
