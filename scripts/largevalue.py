import redis
import sys
import random
import time

seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
data620 = ''.join([seed for i in range(10)])
data6200 = ''.join([seed for i in range(100)])
largedata = ''.join([seed for i in range(500000)])


MAX_KEY = 50000


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
     
    key = "largekey"
    rconn.hset(key, mapping=data)

    while True:
        rconn.hgetall(key)
        
        
        
if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]	

    stress(host, port)
