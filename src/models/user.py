# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property

from src.models.common import Base, engine, Common


csc = 'all,delete,delete-orphan'


class User(Common):
    __tablename__ = 'user'

    id                      = Column(Integer, primary_key=True)

    username                = Column(String(55), unique=True)
    registration_date       = Column(DateTime(timezone=True), server_default=func.now())

    catalog_profiles_num    = Column(Integer, default=1)

    total_txs               = Column(Integer, default=0)
    total_qiwi_sum          = Column(Float, default=0)
    total_btc_sum           = Column(Float, default=0)
    total_girls             = Column(Integer, default=0)

    promocode               = Column(String(20), nullable=True)
    promo_discount          = Column(Integer, nullable=True)
    promo_valid_from        = Column(Date, nullable=True)
    promo_valid_to          = Column(Date, nullable=True)

    girls_filter            = relationship('GirlsFilter', uselist=False, back_populates='user', cascade=csc)
    extended_girls_filter   = relationship('ExtendedGirlsFilter', uselist=False, back_populates='user', cascade=csc)
    services                = relationship('Services', uselist=False, back_populates='user', cascade=csc)

    @hybrid_property
    def days_since_register(self):
        return (datetime.now(timezone.utc) - self.registration_date).days

    @hybrid_property
    def discount_expires_days(self):
        return (self.promo_valid_to - self.promo_valid_from).days

    def __init__(self, username):
        self.username = username


Base.metadata.create_all(engine)
