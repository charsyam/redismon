from redismon.base import db
from redismon.redismon_manager import RedisMonManager
from redismon.redis_info import RedisInfo
from datetime import datetime
import json


class Agent:
    def __init__(self, db):
        self.manager = RedisMonManager(db)
        self.units = self.manager.list_units()
        self.results = []

    def info_all(self):
        now = datetime.utcnow()
        for unit in self.units:
            ri = RedisInfo(unit.addr)
            info = ri.info("all")
            
            self.manager.create_metric(unit.id, json.dumps(info), now)

        self.manager.commit()


if __name__ == '__main__':
    agent = Agent(db)
    agent.info_all()
