import logging
from contextlib import contextmanager
from ipaddress import ip_interface, ip_network

import tenacity
from flask_sqlalchemy import BaseQuery, SQLAlchemy
from sqlalchemy.dialects.postgresql import (
    CIDR,
    ENUM,
    INET,
    JSONB,
)
from sqlalchemy import exc, orm, types
from sqlalchemy_json import NestedMutable


logger = logging.getLogger(__name__)


@contextmanager
def connect(connstring, **kw):
    # Manager for connecting to psycopg2 without flask nor SQLAlchemy.
    import psycopg2
    kw.setdefault('connect_timeout', 5)

    for attempt in tenacity.Retrying(
            reraise=True,
            retry=tenacity.retry_if_exception_type(psycopg2.OperationalError),
            stop=tenacity.stop_after_attempt(10),
            wait=tenacity.wait_fixed(1),
    ):
        with attempt:
            conn = psycopg2.connect(connstring, **kw)

    try:
        yield conn
    finally:
        conn.close()


class CustomQuery(BaseQuery):
    def __init__(self, a0, *a, **kw):
        super().__init__(a0, *a, **kw)
        try:
            # Save model for custom queries.
            self.model = self.m = a0.class_
        except AttributeError:
            pass  # Not a Model.query instance.

    def get_by(self, **kw):
        return self.filter_by(**kw).one()


class IPAddressType(types.TypeDecorator):
    impl = INET

    def process_bind_param(self, value, dialect):
        return str(value) if value else None

    def process_result_value(self, value, dialect):
        return ip_interface(value) if value else None


class IPNetworkType(types.TypeDecorator):
    impl = CIDR

    def process_bind_param(self, value, dialect):
        return str(value) if value else None

    def process_result_value(self, value, dialect):
        return ip_network(value) if value else None

    class comparator_factory(INET.Comparator):
        def intersects(self, other, *_, **__):
            return self.op("&& ", is_comparison=True)(other)


db = SQLAlchemy(query_class=CustomQuery)
db.IPAddress = IPAddressType
db.IPNetwork = IPNetworkType
db.ENUM = ENUM
db.exc = exc
# Our jsonb columns are subject to change and thus, sqlalchemy needs to track
# updates deep in the json. This add nested tracking of mutation of JSON data
# in tuple. See https://github.com/edelooff/sqlalchemy-json/issues/13.
db.JSONB = NestedMutable.as_mutable(JSONB)
db.orm = orm
