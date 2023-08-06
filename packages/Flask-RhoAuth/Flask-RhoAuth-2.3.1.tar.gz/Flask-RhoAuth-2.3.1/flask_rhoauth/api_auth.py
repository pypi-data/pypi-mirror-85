import uuid
from http import HTTPStatus
from functools import wraps
from flask import request, abort
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


class Consumer:
    __tablename__ = 'consumer'

    id = Column(Integer(), primary_key=True)
    custom_id = Column(String(), unique=True)


class ApiKey:
    __tablename__ = 'api_key'
    __related_consumer__ = Consumer

    id = Column(Integer(), primary_key=True)
    key = Column(String(), unique=True, nullable=False,
                 default=str(uuid.uuid4()))

    @declared_attr
    def consumer_id(cls):
        table_name = cls.__related_consumer__.__tablename__
        return Column(Integer(), ForeignKey(table_name + '.id'))

    @declared_attr
    def consumer(cls):
        consumer_name = cls.__related_consumer__.__qualname__
        return relationship(consumer_name, backref="api_keys")

    @classmethod
    def validate_api_key(cls, key):
        try:
            cls.query.filter(cls.key == key).one()
            return True
        except Exception as e:
            return False

    @classmethod
    def apikey_required(cls, fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            api_key = get_api_key()
            if not api_key:
                abort(HTTPStatus.UNAUTHORIZED)

            if cls.validate_api_key(api_key):
                return fn(*args, **kwargs)

            abort(HTTPStatus.UNAUTHORIZED)

        return decorated_view


def get_api_key():
    api_key = request.headers.get('apikey')
    if not api_key:
        api_key = request.args.get('apikey')
    return api_key

