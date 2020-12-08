import redis
import sys

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

    for key in rconn.scan_iter(count=100):
        dtype = rconn.type(key)
        size = dump(rconn, key)

        if size >= limit:
            if size not in all:
                all[size] = []

            all[size].append({"type": dtype.decode(), "key": key.decode()})

    return all


if __name__ == '__main__':
    addr = "localhost"
    limit = 1
    if len(sys.argv) > 1:
        addr = sys.argv[1]
    
    if len(sys.argv) > 2:
        limit = int(sys.argv[2])

    parts = addr.split(':')
    REDIS_PORT = 6379
    if len(parts) >= 1:
        REDIS_HOST = parts[0] 

    if len(parts) >= 2:
        REDIS_PORT = int(parts[1])

    rconn = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
    all = get_all_items_size(rconn, limit)

    for elem in sorted(all.items(), reverse=True) :
        print(elem[0] , " ::" , elem[1] )

