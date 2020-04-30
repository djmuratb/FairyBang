# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Float, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.common import Base, engine


class User(Base):
    __tablename__ = 'user'

    id                  = Column(Integer, primary_key=True)
    username            = Column(String(55), unique=True)
    registration_date   = Column(DateTime(timezone=True), server_default=func.now())
    total_txs           = Column(Integer, default=0)
    total_qiwi_sum      = Column(Float, default=0)
    total_btc_sum       = Column(Float, default=0)
    total_girls         = Column(Integer, default=0)

    girls_filter            = relationship('GirlsFilter', uselist=False, back_populates='user', cascade='all,delete,delete-orphan')
    extended_girls_filter   = relationship('ExtendedGirlsFilter', uselist=False, back_populates='user', cascade='all,delete,delete-orphan')
    services                = relationship('Services', uselist=False, back_populates='user', cascade='all,delete,delete-orphan')

    def __init__(self, username):
        self.username = username


Base.metadata.create_all(engine)
