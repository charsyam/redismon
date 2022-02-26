# redismon
Redis Monitoring Tool

## How to use redismon

* Run Redismon

```
python app.py -a {REDIS_HOST}:{REDIS_PORT}
```

or

* Create Config file
```
[app]
port = 5000
host = 0.0.0.0
elasticache = no

[redis]
host = 192.168.0.102
port = 6379
```

and Run Redismon
```
python app.py -c ./redismon.ini
```
