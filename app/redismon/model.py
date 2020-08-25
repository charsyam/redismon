from redismon.base import db
from sqlalchemy.orm.attributes import QueryableAttribute

import json


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide), 
                        _path=('%s.%s' % (_path, key.lower())),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data


class MonitoringGroup(BaseModel):
    __tablename__ = "monitoring_group"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    seed = db.Column(db.String(256))
    created_at = db.Column(db.DateTime)
    is_cluster = db.Column(db.Boolean)

    _default_fields = [
        "name",
        "seed",
        "is_cluster",
        "created_at"
    ]

    def __init__(self, name, seed, is_cluster, created_at):
        self.name = name
        self.seed = seed
        self.created_at = created_at
        self.is_cluster = is_cluster

    def __repr__(self):
        return f"<MonitoringGroup('{self.id}', '{self.name}', '{self.seed}', '{self.is_cluster}', '{self.created_at}')>"


class Unit(BaseModel):
    __tablename__ = "unit"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(256))
    group_id = db.Column(db.Integer)
    role = db.Column(db.String(16))
    created_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean)
    failure_count = db.Column(db.Integer)

    _default_fields = [
        "addr",
        "group_id",
        "role",
        "is_active",
        "failure_count",
        "created_at",
    ]

    def __init__(self, addr, group_id, role, is_active, failure_count, created_at):
        self.addr = addr
        self.group_id= group_id
        self.role = role
        self.is_active = is_active
        self.failure_count = failure_count
        self.created_at = created_at

    def __repr__(self):
        return f"<Unit('{self.id}', '{self.addr}', '{self.group_id}', '{self.role}', '{self.created_at}')>"


class Metric(BaseModel):
    __tablename__ = "metric"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer)
    value = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    _default_fields = [
        "unit_id",
        "value",
        "created_at"
    ]

    def __init__(self, unit_id, value, created_at):
        self.unit_id = unit_id
        self.value = value
        self.created_at = created_at

    def __repr__(self):
        return f"<Metric('{self.id}', '{self.unit_id}', '{self.value}', '{self.created_at}')>"

class Event(BaseModel):
    __tablename__ = "event"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer)
    last_metric_created_at = db.Column(db.DateTime)
    value = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    _default_fields = [
        "unit_id",
        "value",
        "last_metric_created_at",
        "created_at"
    ]

    def __init__(self, unit_id, last_metric_created_at, value, created_at):
        self.unit_id = unit_id
        self.value = value
        self.last_metric_created_at = last_metric_created_at
        self.created_at = created_at

    def __repr__(self):
        return f"<Event('{self.id}', '{self.unit_id}', '{self.value}', '{self.created_at}')>"
