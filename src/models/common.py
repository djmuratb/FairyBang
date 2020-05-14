# -*- coding: utf-8 -*-
import enum

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.extra import DATABASE


url      = str(URL(**DATABASE))
engine   = create_engine(url)
Base     = declarative_base()


class Common(Base):
    __abstract__ = True

    @staticmethod
    def values_callable(obj):
        return [e.value for e in obj]

    @staticmethod
    def get_column_value(obj, column_key):
        col_val = getattr(obj, column_key)
        if isinstance(col_val, enum.Enum):
            val = col_val.value
        elif isinstance(col_val, str):
            val = str(col_val)
        elif type(col_val) in (tuple, list):
            val = '{} - {}'.format(*col_val)
        else:
            val = 'не задано'

        return val

    @staticmethod
    def get_result_data(obj, column):
        column_value = Common.get_column_value(obj, column.key)
        if column.name == column.key:
            data = (column.key, column_value)
        else:
            data = (column.key, column.name, column_value)

        return data

    @staticmethod
    def as_dict(obj, exclude_columns_names=('id', 'user_id', 'user_username')):
        d = {}
        for column in obj.__table__.columns:
            if column.name in exclude_columns_names:
                continue

            col_val = Common.get_column_value(obj, column.key)
            if column.name == column.key:
                d.update({column.key: col_val})
            else:
                d.update({column.key: {column.name: col_val}})

        return d

    @staticmethod
    def as_list(obj, exclude_columns_names=('id', 'user_id', 'user_username')):
        result = []
        for column in obj.__table__.columns:
            if column.name in exclude_columns_names:
                continue

            result.append(Common.get_result_data(obj, column))

        return result


Session = sessionmaker(bind=engine)
session = Session()
