import redis
import sys

REDIS_HOST = sys.argv[1]
REDIS_PORT = sys.argv[2]

def get_string_key_size(conn, key):
    return len(conn.get("key"))

def get_hash_key_size(conn, key):
    return len(conn.hgetall(key))

def get_set_key_size(conn, key):
    return len(conn.smembers(key))

def dump(conn, key):
    return len(conn.dump(key))

rconn = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

store = {}
for key in rconn.scan_iter(count=100):
    dtype = rconn.type(key)
    size = dump(rconn, key)
    if size not in store:
        store[size] = []

    store[size].append((dtype, key))

for elem in sorted(store.items(), reverse=True) :
    print(elem[0] , " ::" , elem[1] )

