from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types
from sqlalchemy.ext.mutable import Mutable


try:
    import simplejson as json
except ImportError:
    import json

Base = DeclarativeBase = declarative_base()


class JsonType(types.TypeDecorator):
    impl = types.TEXT

    def process_bind_param(self, value, engine):
        if value is None:
            return None

        return json.dumps(value)

    def process_result_value(self, value, engine):
        if value:
            return json.loads(value)
        else:
            # default can also be a list
            return {}


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


class JobStatuses(object):
    PENDING = 'pending'
    SCHEDULED = 'scheduled'
    RUNNING = 'running'
    FAILED = 'failed'
    SUCCESS = 'success'
    ERROR = 'error'

    @classmethod
    def to_list(cls):
        return [
            cls.PENDING, cls.SCHEDULED, cls.RUNNING, cls.FAILED, cls.SUCCESS,
            cls.ERROR
        ]
