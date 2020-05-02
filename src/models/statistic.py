# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Float, Date, Numeric

from src.models.common import Base, engine


class Statistic:
    __tablename__ = 'statistic'

    lauch_date = Column(Date('2020.04.24'))
    total_girls = Column(Integer)
    total_spend_money = Column(Integer)

    def __init__(self):
        pass


Base.metadata.create_all(engine)
