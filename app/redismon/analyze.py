from datetime import datetime, timedelta
from redismon.redismon_manager import RedisMonManager

import json


EPOCH = timedelta(minutes=3)


def explain_get_cmd(key, calls, ptime):
    if ptime >= 10.0:
        print("[WARINING] check some keys have huge data. ptime is {}".format(ptime))


def explain_keys_cmd(key, calls, ptime):
    if calls > 1:
        print("[ERROR] please remove usage of keys command. calls is {}".format(calls))


def explain_client_cmd(key, calls, ptime):
    if ptime > 100.0:
        print("[WARNING] check and reduce connection if you use too many connections. ptime is {}".format(ptime))


def explain_cmd(key, calls, ptime):
    if ptime > 100.0:
        print("[WARNING] check {key}, it is somewhat slow. ptime is {ptime}".format(key=key, ptime=ptime))


EXPLAIN_CMDS_MAP = {
    "cmdstat_get":      explain_get_cmd,
    "cmdstat_keys":     explain_keys_cmd,
    "cmdstat_client":   explain_client_cmd
}


class AnalyzeRedis:
    def __init__(self, manager, addr, metric_from=None, metric_to=None):
        self.addr = addr
        if not metric_from:
            metric_to = datetime.now()
            metric_from = metric_to - timedelta

        self.metric_from = metric_from
        self.metric_to = metric_to
        self.manager = manager

    def analyze(self): 
        unit = self.manager.get_unit_by_addr(self.addr)
        unit_id = unit.id
        metrics = self.manager.get_metrics_by_time_range(unit_id,
                                                         self.metric_from,
                                                         self.metric_to)

        processed_cmds = self.analyze_commands(metrics)
        self.explain(processed_cmds)

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

        return results 
            
    def explain(self, cmds):
        for k, v in cmds.items():
            calls = v[0]
            ptime = v[1]

            if k in EXPLAIN_CMDS_MAP:
                EXPLAIN_CMDS_MAP[k](k, calls, ptime)
            else:
                explain_cmd(k, calls, ptime) 


if __name__ == "__main__":
    from redismon.base import db
    m = RedisMonManager(db)
    ar = AnalyzeRedis(m, "127.0.0.1:6379", datetime(2020, 8, 14, 10), datetime(2020, 8, 14, 18))
    ar.analyze()
