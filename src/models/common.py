# -*- coding: utf-8 -*-
import enum

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src import DATABASE


url      = str(URL(**DATABASE))
engine   = create_engine(url)
Base     = declarative_base()

exclude_columns_names_ = (
    'id',
    'user_id',
    'user_username',
)


class _CommonUtils:

    @staticmethod
    def get_result_data(obj, column):
        column_value = _CommonUtils.get_column_value(obj, column.key)
        return (column.key, column_value) if column.name == column.key else (column.key, column.name, column_value)

    @staticmethod
    def bool_to_special_char(val: bool):
        d = {True: 'да', False: 'нет'}
        return d.get(val)

    @staticmethod
    def get_column_value(obj, column_key):
        col_val = getattr(obj, column_key)
        if isinstance(col_val, enum.Enum):
            val = col_val.value
        elif isinstance(col_val, str):
            val = str(col_val)
        elif type(col_val) in (tuple, list):
            val = '{} - {}'.format(*col_val)
        elif isinstance(col_val, bool):
            val = _CommonUtils.bool_to_special_char(col_val)
        else:
            val = 'не задано'

        return val


class Common(Base):
    __abstract__ = True

    @staticmethod
    def as_dict(obj, exclude_columns_names=exclude_columns_names_):
        d = {}
        for column in obj.__table__.columns:
            if column.name in exclude_columns_names:
                continue

            col_val = _CommonUtils.get_column_value(obj, column.key)
            if column.name == column.key:
                d.update({column.key: col_val})
            else:
                d.update({column.key: {column.name: col_val}})

        return d

    @staticmethod
    def as_list(obj, exclude_columns_names=exclude_columns_names_):
        result = []
        for column in obj.__table__.columns:
            if column.name in exclude_columns_names:
                continue

            result.append(_CommonUtils.get_result_data(obj, column))

        return result

    @staticmethod
    def values_callable(obj):
        return [e.value for e in obj]


Session = sessionmaker(bind=engine)
session = Session()
