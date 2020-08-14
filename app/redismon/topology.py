import redis
import sys


MASTER_KEY      = "master"
ROLE_KEY        = "role"
SLAVES_KEY      = "connected_slaves"
SLAVE_KEY       = "slave"


class Topology:
    def __init__(self, addr):
        host, port = self.get_host_and_port(addr)
        self.results = self.parse_topology(self.get_top_master(host, port))

    def get_topology(self):
        return self.results

    def get_host_and_port(self, addr):
        parts = addr.split(":")
        return parts[0], int(parts[1])

    def parse_slaves_info(self, info):
        slaves_info = {}

        count = int(info[SLAVES_KEY]) if SLAVES_KEY in info else 0

        for i in range(count):
            slaveN = "slave{}".format(i)
            slave = info[slaveN]
            slaves_info[slaveN] = slave

        return slaves_info

    def parse_master_info(self, info):
        master_info = {}
        if info["role"] == SLAVE_KEY:
            master_info["host"] = info["master_host"]
            master_info["port"] = info["master_port"]
            master_info["link_status"] = info["master_link_status"]

        return master_info

    def get_top_master(self, host, port):
        conn = redis.StrictRedis(host, port)
        info = conn.info()

        role = info[ROLE_KEY]
        if role == MASTER_KEY:
            return (host, port)

        minfo = self.parse_master_info(info)
        return self.get_top_master(minfo["host"], minfo["port"])

    def parse_slave_node(self, host, port, parent, results):
        conn = redis.StrictRedis(host, port)
        info = conn.info()
        sinfo = self.parse_slaves_info(info)

        addr = "{host}:{port}".format(host=host, port=port)
        host_info = {"type": "slave", "host": host, "port": port, "parent": parent}

        results.append(host_info)
        for k in sinfo.keys():
            self.parse_slave_node(sinfo[k]["ip"], sinfo[k]["port"], addr, results)

    def parse_topology(self, addr):
        host, port = addr
        conn = redis.StrictRedis(host=host, port=port)
        info = conn.info()

        sinfo = self.parse_slaves_info(info)

        addr = "{host}:{port}".format(host=host, port=port)
        host_info = {"type": "master", "host": host, "port": port}

        results = []
        results.append(host_info)

        for k in sinfo.keys():
            self.parse_slave_node(sinfo[k]["ip"], sinfo[k]["port"], addr, results)

        return results


if __name__ == "__main__":
    t = Topology(sys.argv[1])
    print(t.get_topology())
