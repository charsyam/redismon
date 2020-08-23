import redis


class RedisInfo:
    def __init__(self, addr):
        self.addr = addr
        parts = addr.split(':')
        self.conn = redis.StrictRedis(parts[0], int(parts[1]))

    def is_cluster(self):
        info = self.info()
        if "cluster_enabled" in info and info["cluster_enabled"] == 1:
            return True

        return False

    def info(self, cmd = "all"):
        return self.conn.info(cmd)

    def is_master(self):
        info = self.info()
        if info["role"] == "master":
            return True

        return False


if __name__ == '__main__':
    import sys
    ri = RedisInfo(sys.argv[1])
    print(ri.info())
