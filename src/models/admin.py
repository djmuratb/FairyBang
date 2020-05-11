# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Float, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from src.models.common import Base, engine


class Admin:
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)

    statistic = relationship('Statistic', uselist=False, back_populates='admin', cascade='all,delete,delete-orphan')

    def __init__(self):
        pass


class Statistic:
    __tablename__ = 'statistic'

    launch_date             = Column(Date, default='2020.04.24')
    total_girls             = Column(Integer)
    total_spend_money       = Column(Integer)

    admin_id = Column(Integer, ForeignKey('admin.id', ondelete='CASCADE'))

    def __init__(self):
        pass


Base.metadata.create_all(engine)
