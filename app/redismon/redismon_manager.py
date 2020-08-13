from redismon.model import MonitoringGroup

class RedisMonManager:
    def __init__(self, db):
        self.db = db

    def create_monitoring_group(self, name, seed):
        group = MonitoringGroup(name, seed)        
        self.db.session.add(group)
        self.db.session.commit()
        return group

    def list_monitoring_groups(self):
        return MonitoringGroup.query.all()

    def delete_monitoring_group(self, group_id):
        MonitoringGroup.query.filter(MonitoringGroup.id == group_id).delete()

