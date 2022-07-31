import collections
import redis
import sys
import time


keys = [
    "instantaneous_input_kbps",
    "instantaneous_output_kbps",
    "instantaneous_input_repl_kbps",
    "instantaneous_output_repl_kbps",
    "total_net_input_bytes",
    "total_net_output_bytes",
    "total_net_repl_input_bytes",
    "total_net_repl_output_bytes",
]

def check_network(conn):
    value = conn.info()

    results = {}
    for key in keys:
        results[key] = value[key]

    return results


if  __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    rconn = redis.StrictRedis(host=host, port=port, db=0)

    while(True):
        print(check_network(rconn))
        time.sleep(3)
