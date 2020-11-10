import json


PTIME = "ptime"
CALLS = "calls"

def explain_slow_cmd(cmd, calls, ptime, call_limit, ptime_limit):
    if ptime >= ptime_limit:
        return {'cmd': cmd, 'value': ptime, 'type': PTIME,
                'description': "some keys have large value"}


def explain_ON_cmd(cmd, calls, ptime, call_limit, ptime_limit):
    if ptime >= ptime_limit:
        return {'cmd': cmd, 'value': ptime, 'type': CALLS,
                'description': "You may get all data from large collections"}


def explain_keys_cmd(cmd, calls, ptime, call_limit, ptime_limit):
    if calls > call_limit:
        return {'cmd': cmd, 'value': calls, 'type': CALLS,
                'description': "Don't use keys command"}

def explain_client_cmd(cmd, calls, ptime, call_limit, ptime_limit):
    if ptime > ptime_limit:
        return {'cmd': cmd, 'value': ptime, 'type': CALLS,
                'description': " You have too many connections."}

def explain_cluster_cmd(cmd, calls, ptime, call_limit, ptime_limit):
    if ptime > ptime_limit:
        return {'cmd': cmd, 'value': ptime, 'type': PTIME,
                'description': "cluster command is basically slow command."}


EXPLAIN_CMDS_MAP = {
    "cmdstat_get":      (explain_slow_cmd, 0, 10.0),
    "cmdstat_hget":      (explain_slow_cmd, 0, 10.0),
    "cmdstat_hmget":      (explain_slow_cmd, 0, 10.0),
    "cmdstat_keys":     (explain_keys_cmd, 1, 0.0),
    "cmdstat_client":   (explain_client_cmd, 0, 100.0),
    "cmdstat_hgetall":  (explain_ON_cmd, 0, 50.0),
    "cmdstat_hvals":  (explain_ON_cmd, 0, 50.0),
    "cmdstat_smembers":  (explain_ON_cmd, 0, 50.0),
    "cmdstat_zrange":  (explain_ON_cmd, 0, 50.0),
    "cmdstat_zrangebyscore":  (explain_ON_cmd, 0, 50.0),
    "cmdstat_zrevrange":  (explain_ON_cmd, 0, 50.0),
    "cmdstat_zrevrangebyscore":  (explain_ON_cmd, 0, 50.0),
    "cmdstat_cluster":  (explain_cluster_cmd, 0, 50.0),
}


class RedisExplainer:
    def __init__(self, values):
        self.values = values

    def explain(self):
        cmds = self.analyze_commands(self.values)
        return self.explain_commands(cmds)

    def explain_commands(self, cmds):
        results = []
        for k, v in cmds.items():
            calls = v[0]
            ptime = v[1]

            call = explain_slow_cmd
            call_limit = 0
            ptime_limit = 100

            if k in EXPLAIN_CMDS_MAP:
                m = EXPLAIN_CMDS_MAP[k]
                call = m[0]
                call_limit = m[1]
                ptime_limit = m[2]

            ret = call(k, calls, ptime, call_limit, ptime_limit)
            if ret is not None:
                results.append(ret)

        return results

    def get_commands(self, info):
        cmds = []

        for key in info.keys():
            if key.startswith("cmdstat_"):
                cmds.append((key, info[key]))

        return cmds

    def analyze_commands(self, values):
        cmds = []
        for value in values:
            cmds.append(self.get_commands(value))

        results = {}
        for i in range(len(cmds) - 1):
            current_cmds = cmds[i]
            next_cmds = cmds[i+1]

            cmdMap = {k:v for k, v in current_cmds}
            for cmd in next_cmds:
                k = cmd[0]
                v = cmd[1]

                if k in cmdMap:
                    v1 = cmdMap[k]
                    results[k] = (v["calls"] - v1["calls"], v["usec_per_call"])
                else:
                    results[k] = (v["calls"], v["user_per_call"])

        return results
