# -*- coding: utf-8 -*-
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

    def as_dict(self, obj, exclude_columns_names=('id', 'user_id')):
        d = {}
        for column in obj.__table__.columns:
            if column.name in exclude_columns_names:
                continue

            if column.name == column.key:
                d.update({column.key: getattr(obj, column.key)})
            else:
                d.update({column.key: {column.name: getattr(obj, column.key)}})

        return d


    def as_list(self, obj, exclude_columns_names=('id', 'user_id'), calc_str_size=False):
        l = []
        for column in obj.__table__.columns:
            if column.name in exclude_columns_names:
                continue

            if column.name == column.key:
                l.append([column.key, str(getattr(obj, column.key))])
            else:
                l.append([column.key, column.name, str(getattr(obj, column.key))])

        return l


Session = sessionmaker(bind=engine)
session = Session()
