from datetime import datetime, timedelta
from redismon.redismon_manager import RedisMonManager

import json


EPOCH = timedelta(minutes=30)

WARNING = "WARNING"
ERROR = "ERROR"


def explain_slow_cmd(cmd, calls, ptime, call_limit, ptime_limit):
    if ptime >= ptime_limit:
        return f"[{WARNING}:{cmd}:{ptime}] some keys have large value."

def explain_ON_cmd(cmd, calls, ptime, call_limit, ptime_limit):
    if ptime >= ptime_limit:
        return f"[{WARNING}:{cmd}:{ptime}] You may get all data from large collections"

def explain_keys_cmd(cmd, calls, ptime, call_limit, ptime_limit):
    if calls > call_limit:
        return f"[{ERROR}:{cmd}:{calls}] Don't use keys command."

def explain_client_cmd(cmd, calls, ptime, call_limit, ptime_limit):
    if ptime > ptime_limit:
        return f"[{WARNING}:{cmd}:{ptime}] You have too many connections."

def explain_cluster_cmd(cmd, calls, ptime, call_limit, ptime_limit):
    if ptime > ptime_limit:
        return f"[{WARNING}:{cmd}:{ptime}] cluster command is basically slow command."

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


class RedisAnalyzer:
    def __init__(self, unit, metrics):
        self.unit = unit
        self.metrics = metrics

    def analyze(self): 
        if len(self.metrics) == 0:
            return (None, None)

        processed_cmds = self.analyze_commands(self.metrics)
        return (self.metrics[-1].created_at, self.explain(processed_cmds))

    def get_commands(self, info):
        cmds = []

        for key in info.keys():
            if key.startswith("cmdstat_"):
                cmds.append((key, info[key]))

        return cmds

    def analyze_commands(self, metrics):
        cmds = []
        for metric in metrics:
            cmds.append(self.get_commands(json.loads(metric.value)))

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
                else:
                    results[k] = (v["calls"], v["user_per_call"])

        print(self.unit.addr, results)
        return results 
            
    def explain(self, cmds):
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

        return "\n".join(results)


class AnalyzerManager:
    def __init__(self, manager):
        self.manager = manager

    def analyzeRedis(self, unit, metrics):
        analyzer = RedisAnalyzer(unit, metrics)
        return analyzer.analyze()

    def analyze(self, metric_from=None, metric_to=None):
        units = self.manager.list_units()
        now = datetime.utcnow()
        if not metric_from:
            metric_to = now
            metric_from = metric_to - EPOCH

        for unit in units:
            metrics = self.manager.get_metrics_by_time_range(unit.id,
                                                             metric_from,
                                                             metric_to)
            if len(metrics) > 0:
                last_metric_created_at, value = self.analyzeRedis(unit, metrics)
                if last_metric_created_at != None:
                    event = self.manager.create_event(unit.id, last_metric_created_at, value, now)
                    print(event)


        self.manager.commit()


if __name__ == "__main__":
    from redismon.base import db
    m = RedisMonManager(db)
    arm = AnalyzerManager(m)
    arm.analyze()
