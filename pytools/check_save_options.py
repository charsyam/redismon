import collections
import redis
import sys


if  __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    rconn = redis.StrictRedis(host=host, port=port, db=0)
    value = rconn.config_get("save")["save"]

    if len(value) > 0:
        print(f"Please check save option, It will cause performance degrations: {value}")
        print("You can remove save option: config set save \"\"")
    else:
        print(f"No save options")
