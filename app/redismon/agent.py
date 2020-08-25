from redismon.base import db
from redismon.redismon_manager import RedisMonManager
from redismon.redis_info import RedisInfo
from datetime import datetime
import json


FAILURE_LIMIT = 3

class Agent:
    def __init__(self, db):
        self.manager = RedisMonManager(db)
        self.units = self.manager.list_units()
        self.results = []

    def info_all(self):
        now = datetime.utcnow()
        for unit in self.units:
            try:
                ri = RedisInfo(unit.addr)
                info = ri.info("all")
                self.manager.create_metric(unit.id, json.dumps(info), now)
                if unit.is_active is False:
                    unit.is_active = True
                    unit.failure_count = 0
            except Exception as ex:
                print(ex)
                unit.failure_count += 1
                if unit.failure_count == FAILURE_LIMIT:
                    unit.is_active = False

        self.manager.commit()


if __name__ == '__main__':
    agent = Agent(db)
    agent.info_all()
