import redis
import sys
import random

seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
data620 = ''.join([seed for i in range(10)])
data6200 = ''.join([seed for i in range(100)])
data6200000 = ''.join([seed for i in range(100000)])


MAX_KEY = 1000


def gen_data():
    tdata = {}
    for i in range(MAX_KEY):
        key = f"key{i}"
        tdata[key] = data620    
        if i % 10 == 0:
            tdata[key] = data6200

    return tdata


data = gen_data()


def stress(host, port):
    global data
    rconn = redis.StrictRedis(host, port)
     
    for i in range(MAX_KEY):
        key = f"key{i}"
        rconn.set(key, data[key])

    while True:
        k = random.randint(0, MAX_KEY-1)
        p = random.randint(0, 100)

        key = f"key{k}"
        if p > 80:
            rconn.set(key, data[key])
        else:
            rconn.get(key)
        
        
        
if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]	

    stress(host, port)
