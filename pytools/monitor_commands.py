import collections
import redis
import sys


class Monitor():
    def __init__(self, connection_pool):
        self.key_counter = collections.Counter()
        self.connection_pool = connection_pool
        self.connection = None
        self.run = True

    def __del__(self):
        try:
            self.reset()
        except:
            pass

    def reset(self):
        if self.connection:
            self.connection_pool.release(self.connection)
            self.connection = None

    def monitor(self):
        if self.connection is None:
            self.connection = self.connection_pool.get_connection(
                'monitor', None)
        self.connection.send_command("monitor")
        return self.listen()

    def parse_response(self):
        return self.connection.read_response()

    def listen(self):
        while self.run:
            try:
                yield self.parse(self.parse_response())
            except:
                self.run = False

    def parse(self, response):
        value = response.decode('utf-8').replace("\"", "")
        parts = value.split()
        if len(parts) > 4:
            db = parts[1][1:]
            host = parts[2][:-1]
            cmd = parts[3].lower()
            key = parts[4]

            if cmd not in ["info"]:
                self.key_counter[key] += 1

        return response
        

if  __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    pool = redis.ConnectionPool(host=host, port=port, db=0)
    monitor = Monitor(pool)
    commands = monitor.monitor()

    for c in commands :
        if monitor.run == False:
            print("")
            break

        print(c)

    monitor.reset()
    top100 = monitor.key_counter.most_common(100)
    conn = redis.StrictRedis(host, port)
    for key, count in top100:
        data = conn.dump(key)
        size = len(data)
        print(key, count, size)
        
