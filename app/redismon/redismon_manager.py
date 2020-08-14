from redismon.model import MonitoringGroup, Unit
from redismon.topology import Topology
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

