from datetime import datetime, timedelta
from redismon.redismon_manager import RedisMonManager

import json
import sys

from scipy import stats

class RedisAbnormalDetection:
    def __init__(self, metrics1, metrics2):
        self.metrics1 = metrics1
        self.metrics2 = metrics2

    def check(self): 
        l1 = len(self.metrics1)
        l2 = len(self.metrics2)

        if l1 == 0 or l2 == 0:
            return None

        m = min(l1, l2)
        m1 = self.metrics1[:m]
        m2 = self.metrics2[:m]

        a = self.extract_commands(m1, "info")
        b = self.extract_commands(m2, "info")

        print(a)
        print(b)

        desc_a = stats.describe(a)
        desc_b = stats.describe(b)

        print("a/b-> 평균: {0:.3}/{1:.3}, 분산: {2:.3}/{3:.3}".format(desc_a.mean, desc_b.mean, desc_a.variance, desc_b.variance))

        # 대응표본 t 검정
        t = stats.ttest_rel(a,b)
        print("t-dep-test p-value: {0:.12f}, {1}".format(t.pvalue, t.statistic))

        

    def get_commands(self, info, prefix, cmds):
        for key in info.keys():
            if key.startswith("cmdstat_" + prefix):
                #cmds.append((key, info[key]))
                cmds.append(info[key]["usec_per_call"])

    def extract_commands(self, metrics, key):
        cmds = []
        for m in metrics:
            self.get_commands(json.loads(m.value), key, cmds)

        return cmds


class AnalyzerManager:
    def __init__(self, manager):
        self.manager = manager

    def analyze(self, unit, metrics1_from=None, metrics1_to=None, metrics2_from=None, metrics2_to=None):
        m1 = self.fetch_with_range(unit, metrics1_from, metrics1_to)
        m2 = self.fetch_with_range(unit, metrics2_from, metrics2_to)

        return m1, m2

    def fetch_with_range(self, unit_id, metric_from, metric_to):
        units = self.manager.list_units()
        metrics = self.manager.get_all_metrics_by_time_range(unit_id,
                                                         metric_from,
                                                         metric_to)

        return metrics


unit_id = int(sys.argv[1])

if __name__ == "__main__":
    from redismon.base import db
    m = RedisMonManager(db)
    arm = AnalyzerManager(m)
    
    t1 = sys.argv[2]
    t2 = sys.argv[3]
    t3 = sys.argv[4]
    t4 = sys.argv[5]

    m1, m2 = arm.analyze(unit_id, t1, t2, t3, t4)

    r = RedisAbnormalDetection(m1, m2)
    r.check()
