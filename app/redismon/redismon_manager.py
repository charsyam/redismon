from redismon.model import MonitoringGroup, Unit, Metric, Event
from redismon.topology import TopologyManager
from redismon.redis_info import RedisInfo
from sqlalchemy.sql import text
from datetime import datetime


class RedisMonManager:
    def __init__(self, db):
        self.db = db

    def create_monitoring_group(self, name, seed):
        now = datetime.utcnow()
        
        info = RedisInfo(seed)

        is_cluster = info.is_cluster()
        group = MonitoringGroup(name, seed, is_cluster, now)

        self.db.session.add(group)
        self.commit()

        topology = TopologyManager(seed)
        for host in topology.get_topology():
            addr = "{host}:{port}".format(host=host["host"], port=host["port"])
            self.create_unit(group.id, addr, host["role"], True, 0, now)

        self.commit()
        return group

    def list_monitoring_groups(self):
        return MonitoringGroup.query.all()

    def delete_monitoring_group(self, group_id):
        MonitoringGroup.query.filter(MonitoringGroup.id == group_id).delete()

    def get_unit_by_addr(self, addr):
        return Unit.query.filter(Unit.addr == addr).one()

    def get_all_metrics_by_time_range(self, unit_id, time_from, time_to):
        return Metric.query.filter(Metric.created_at.between(time_from, time_to)).all()

    def get_metrics_by_time_range(self, unit_id, time_from, time_to):
        query = text("SELECT min(id) as min_id, max(id) as max_id FROM metric WHERE unit_id=:unit_id and created_at between :tfrom and :tto")
        result = self.db.session.query("min_id", "max_id")\
                                .from_statement(query)\
                                .params(unit_id=unit_id, tfrom=time_from, tto=time_to).one()

        return Metric.query.filter(Metric.id.in_(result)).all()

    def create_metric(self, unit_id, value, now, commit=True):
        metric = Metric(unit_id, value, now)
        self.db.session.add(metric)
        if commit:
            self.db.session.commit()

        return metric

    def create_event(self, unit_id, last_metric_created_at,  value, now, commit=True):
        event = Event(unit_id, last_metric_created_at, value, now)
        self.db.session.add(event)
        if commit:
            self.db.session.commit()

        return event

    def create_unit(self, group_id, addr, role, is_active, failure_count, now, commit=True):
        unit = Unit(addr, group_id, role, is_active, failure_count, now)
        self.db.session.add(unit)
        if commit:
            self.db.session.commit()

        return unit

    def list_units(self):
        return Unit.query.all()

    def commit(self):
        self.db.session.commit()


if __name__ == '__main__':
    from redismon.base import db
    m = RedisMonManager(db)
    unit = m.get_unit_by_addr("127.0.0.1:6379")
    print(unit)
    metrics = m.get_metrics_by_time_range(4, datetime(2020, 8, 14, 10), datetime(2020, 8, 14, 18)) 
    print(metrics)
