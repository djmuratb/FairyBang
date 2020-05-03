# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.extra import DATABASE


engine = create_engine(URL(**DATABASE))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
