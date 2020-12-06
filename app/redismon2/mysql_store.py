from sqlalchemy import text
from model import Metric


class MysqlStore:
    def __init__(self, session, limit = 120):
        self.session = session
        self.limit = limit

    def append(self, value):
        m = Metric(value)
        self.session.add(m)
        self.session.commit()

    def get(self):
        sql = text(f'select max(id) as max_id from {Metric.__tablename__}')
        max_id = self.session.query("max_id").from_statement(sql).one()[0]
        values = []
        if max_id:
            metrics = Metric.query.filter(Metric.id.between(max_id-120, max_id)).all()
            values = [m.value for m in metrics]

        return values
