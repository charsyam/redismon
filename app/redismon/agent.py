from redismon.model import Unit, Metric
from redismon.base import db
from datetime import datetime
import json
import redis


class Agent:
    def __init__(self, db, units):
        self.db = db
        self.units = units
        self.results = []

    def info_all(self):
        now = datetime.utcnow()
        for unit in self.units:
            parts = unit.addr.split(":")
            rconn = redis.StrictRedis(parts[0], int(parts[1]))
            info = self.info_all_each(rconn)
            
            metric = Metric(unit.id, json.dumps(info), now)
            self.db.session.add(metric)

        self.db.session.commit()
            

    def info_all_each(self, rconn):
        info = rconn.info("all")
        return info

if __name__ == '__main__':
    units = Unit.query.all()
    agent = Agent(db, units)
    agent.info_all()
