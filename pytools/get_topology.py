import redis
import sys
import json

HOST=sys.argv[1]
PORT=sys.argv[2]

MASTER_KEY      = "master"
ROLE_KEY        = "role"
SLAVES_KEY      = "connected_slaves" 
SLAVE_KEY       = "slave"
"""
role master
connected_slaves 2
slave0 {'ip': '127.0.0.1', 'port': 6380, 'state': 'online', 'offset': 924, 'lag': 1}
slave1 {'ip': '127.0.0.1', 'port': 6381, 'state': 'online', 'offset': 924, 'lag': 1}
"""
def parse_slaves_info(info):
    slaves_info = {}

    count = int(info[SLAVES_KEY]) if SLAVES_KEY in info else 0

    for i in range(count):
        slaveN = "slave{}".format(i)
        slave = info[slaveN]
        slaves_info[slaveN] = slave

    return slaves_info

def parse_master_info(info):
    master_info = {}
    if info["role"] == SLAVE_KEY:
        master_info["host"] = info["master_host"]
        master_info["port"] = info["master_port"]
        master_info["link_status"] = info["master_link_status"]
    
    return master_info


def get_top_master(host, port):
    conn = redis.StrictRedis(host, port)
    info = conn.info()

    role = info[ROLE_KEY]
    if role == MASTER_KEY:
        return (host, port)

    minfo = parse_master_info(info)
    return get_top_master(minfo["host"], minfo["port"])

def parse_slave_node(host, port, parent, results):
    conn = redis.StrictRedis(host, port)

    info = conn.info()
    sinfo = parse_slaves_info(info)

    addr = "{host}:{port}".format(host=host, port=port)
    host_info = {"type": "slave", "host": host, "port": port, "parent": parent}

    results[addr] = host_info
    for k in sinfo.keys():
        parse_slave_node(sinfo[k]["ip"], sinfo[k]["port"], addr, results)

def parse_redis_topology(master):
    host = master[0]
    port = master[1]

    conn = redis.StrictRedis(host, port)
    info = conn.info()
    sinfo = parse_slaves_info(info)

    addr = "{host}:{port}".format(host=host, port=port)
    host_info = {"type": "master", "host": host, "port": port}

    results = {}
    results[addr] = host_info

    for k in sinfo.keys():
        parse_slave_node(sinfo[k]["ip"], sinfo[k]["port"], addr, results)

    return results
        

if __name__ == "__main__":
    print(parse_redis_topology(get_top_master(HOST, PORT)))
