import redis
import sys
import time

REDIS_HOST = sys.argv[1]
REDIS_PORT = sys.argv[2]
COLLECT_COUNT = 3
SLEEP_TIME = 3


"""
cmdstat_get (0, 1.9)
cmdstat_set (0, 950.0)
cmdstat_hmget (0, 3.8)
cmdstat_setex (0, 6.2)
cmdstat_select (0, 1.17)
cmdstat_client (0, 1.17)
cmdstat_info (1, 318.11)
cmdstat_exists (0, 1.0)
"""


def explain_get_cmd(key, calls, ptime):
    if ptime >= 10.0:
        print("[WARINING] check some keys have huge data.")


def explain_keys_cmd(key, calls, ptime):
    if calls > 1:
        print("[ERROR] please remove usage of keys command.")


def explain_client_cmd(key, calls, ptime):
    if ptime > 100.0:
        print("[WARNING] check and reduce connection if you use too many connections.")


def explain_cmd(key, calls, ptime):
    if ptime > 100.0:
        print("[WARNING] check {key}, it is somewhat slow.".format(key=key))


EXPLAIN_CMDS_MAP = {
    "cmdstat_get":      explain_get_cmd,
    "cmdstat_keys":     explain_keys_cmd,
    "cmdstat_client":   explain_client_cmd
}


def explain(cmds):
    for k, v in cmds.items():
        calls = v[0]
        ptime = v[1]

        if k in EXPLAIN_CMDS_MAP:
            EXPLAIN_CMDS_MAP[k](k, calls, ptime)
        else:
            explain_cmd(k, calls, ptime)


def get_conn(host, port):
    return redis.StrictRedis(host, port)


def get_commands(conn):
    info = conn.info("all")
    cmds = []
    for key in info.keys():
        if key.startswith("cmdstat_"):
            cmds.append((key, info[key]))

    return cmds


def calculate_processed_time(cmds):
    results = {}
    for i in range(len(cmds)-1):
        current_cmds = cmds[i]
        next_cmds = cmds[i+1]

        cmdMap = {k:v for k,v in current_cmds}
        for cmd in next_cmds:
            k = cmd[0]
            v = cmd[1]

            if k in cmdMap:
                v1 = cmdMap[k]
                results[k] = (v["calls"] - v1["calls"], v["usec_per_call"])

    return results


def analyze_redis(conn):
    cmds = []
    for i in range(COLLECT_COUNT):
        cmds.append(get_commands(conn))
        time.sleep(SLEEP_TIME)

    processed_cmds = calculate_processed_time(cmds)
    return processed_cmds


if __name__ == "__main__":
    conn = get_conn(REDIS_HOST, REDIS_PORT)
    results = analyze_redis(conn)
    explain(results)
