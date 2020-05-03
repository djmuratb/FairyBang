# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.extra import DATABASE


engine = create_engine(str(URL(**DATABASE)))
Base = declarative_base()

class Common(Base):
    __abstract__ = True

    def as_dict(self, obj, exclude_columns_names=('id', 'user_id')):
        return {
            column.name: getattr(obj, column.key)
            for column in obj.__table__.columns
            if column.name not in exlude_columns_names
        }

Session = sessionmaker(bind=engine)
session = Session()
