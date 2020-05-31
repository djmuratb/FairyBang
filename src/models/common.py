# -*- coding: utf-8 -*-
import enum

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src import USERS_DB, GIRLS_DB


url_user      = str(URL(**USERS_DB))
engine_user   = create_engine(url_user)
BaseUser      = declarative_base()

url_girl      = str(URL(**GIRLS_DB))
engine_girl   = create_engine(url_girl)
BaseGirl      = declarative_base()

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


class Common:

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
    def as_genexpr(obj, exclude_columns_names=exclude_columns_names_):
        return (
            _CommonUtils.get_result_data(obj, column)
            for column in obj.__table__.columns
            if column.name not in exclude_columns_names
        )

    @staticmethod
    def as_tuple(obj, exclude_columns_names=exclude_columns_names_):
        return tuple(Common.as_genexpr(obj, exclude_columns_names))

    @staticmethod
    def values_callable(obj):
        return [e.value for e in obj]


class UserBase(BaseUser, Common):
    __abstract__ = True


class GirlBase(BaseGirl, Common):
    __abstract__ = True


UserSession = sessionmaker(bind=engine_user)
user_session = UserSession()

GirlSession = sessionmaker(bind=engine_girl)
girl_session = GirlSession()
