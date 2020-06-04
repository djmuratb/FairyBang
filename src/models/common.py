# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.sql.sqltypes import INTEGER, VARCHAR, BOOLEAN
from sqlalchemy.dialects.postgresql.base import ENUM
from sqlalchemy.dialects.postgresql.array import ARRAY

from src import USERS_DB, GIRLS_DB
from src.core.helpers.types import ColumnResultSet


meta          = MetaData()
url_user      = str(URL(**USERS_DB))
engine_user   = create_engine(url_user)
meta.reflect(bind=engine_user)
BaseUser      = declarative_base()

url_girl      = str(URL(**GIRLS_DB))
engine_girl   = create_engine(url_girl)
BaseGirl      = declarative_base()

EXCLUDE_BY_DEFAULT = (
    'id',
    'user_id',
    'user_username',
)


class _CommonUtils:

    @staticmethod
    def get_column_type_class(column, table_name):
        for table in meta.sorted_tables:
            if table.name == table_name:
                return type(table.columns[column.name].type)

    @staticmethod
    def create_column_result_set(instance, column):
        col_type, col_val = _CommonUtils.get_value_and_type(instance, column)
        return ColumnResultSet(
            key=column.key,
            name=column.name,
            value=col_val,
            type=col_type,
        )

    @staticmethod
    def bool_to_special_char(val: bool):
        d = {True: 'да', False: 'нет'}
        return d.get(val)

    @staticmethod
    def get_value_and_type(instance, column):
        """
        :param instance:
        :param column:
        :return: value and type from specific column of instance.
        """
        col_type = _CommonUtils.get_column_type_class(column, instance.__class__.__table__.name)
        col_val = getattr(instance, column.key)

        if col_val is None:
            val = 'не задано'
        elif col_type is INTEGER:
            val = str(col_val)
        elif col_type is VARCHAR:
            val = col_val
        elif col_type is BOOLEAN:
            val = _CommonUtils.bool_to_special_char(col_val)
        elif col_type is ENUM:
            val = col_val.value
        elif col_type is ARRAY:
            val = '{} - {}'.format(*col_val)
        else:
            raise Exception('Invalid column type.')

        return col_type, val


class Common:

    @staticmethod
    def as_dict(instance, exclude_columns_names=EXCLUDE_BY_DEFAULT):
        pass

    @staticmethod
    def as_genexpr(instance, exclude_columns_names=EXCLUDE_BY_DEFAULT):
        return (
            _CommonUtils.create_column_result_set(instance, column)
            for column in instance.__table__.columns
            if column.name not in exclude_columns_names
        )

    @staticmethod
    def as_tuple(instance, exclude_columns_names=EXCLUDE_BY_DEFAULT):
        return tuple(Common.as_genexpr(instance, exclude_columns_names))

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
