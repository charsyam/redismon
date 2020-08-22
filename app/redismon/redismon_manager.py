from redismon.model import MonitoringGroup, Unit, Metric
from redismon.topology import Topology
from sqlalchemy.sql import text
from datetime import datetime


class RedisMonManager:
    def __init__(self, db):
        self.db = db

    def create_monitoring_group(self, name, seed):
        now = datetime.utcnow()
        group = MonitoringGroup(name, seed, now)
        
        self.db.session.add(group)
        self.db.session.commit()

        topology = Topology(seed)
        for unit in topology.get_topology():
            addr = "{host}:{port}".format(host=unit["host"], port=unit["port"])
            unit = Unit(addr, group.id, now)
            self.db.session.add(unit)

        self.db.session.commit()
        
        return group

    def list_monitoring_groups(self):
        return MonitoringGroup.query.all()

    def delete_monitoring_group(self, group_id):
        MonitoringGroup.query.filter(MonitoringGroup.id == group_id).delete()

    def get_unit_by_addr(self, addr):
        return Unit.query.filter(Unit.addr == addr).one()

    def get_metrics_by_time_range(self, unit_id, time_from, time_to):
        query = text("SELECT min(id) as min_id, max(id) as max_id FROM metric WHERE created_at between :tfrom and :tto")
        result = self.db.session.query("min_id", "max_id")\
                                .from_statement(query)\
                                .params(tfrom=time_from, tto=time_to).one()

        return Metric.query.filter(Metric.id.in_(result)).all()



if __name__ == '__main__':
    from redismon.base import db
    m = RedisMonManager(db)
    unit = m.get_unit_by_addr("127.0.0.1:6379")
    print(unit)
    metrics = m.get_metrics_by_time_range(4, datetime(2020, 8, 14, 10), datetime(2020, 8, 14, 18)) 
    print(metrics)
