# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property

from src.models.common import Base, engine, Common
from src.models.base import BaseFilter, ExtFilter, Services


csc = 'all,delete,delete-orphan'


class UserGirlServices(Services):
    __tablename__ = 'users_girl_services'

    #           --- relationship ---
    user_username   = Column(String(50), ForeignKey('users.username', ondelete='CASCADE'))
    user            = relationship('User', back_populates='services')

    def __init__(self):
        pass


class UserGirlExtFilter(ExtFilter):
    __tablename__ = 'users_girl_ext_filter'

    #       --- relationship ---
    user_username   = Column(String(50), ForeignKey('users.username', ondelete='CASCADE'))
    user            = relationship('User', back_populates='ext_filter')

    def __init__(self):
        pass


class UserGirlBaseFilter(BaseFilter):
    __tablename__ = 'users_girl_base_filter'

    #       --- relationship ---
    user_username   = Column(String(50), ForeignKey('users.username', ondelete='CASCADE'))
    user            = relationship('User', back_populates='base_filter')

    def __init__(self):
        pass


class User(Common):
    __tablename__ = 'users'

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

    base_filter             = relationship('UserGirlBaseFilter', uselist=False, back_populates='user', cascade=csc)
    ext_filter              = relationship('UserGirlExtFilter', uselist=False, back_populates='user', cascade=csc)
    services                = relationship('UserGirlServices', uselist=False, back_populates='user', cascade=csc)

    @hybrid_property
    def days_since_register(self):
        return (datetime.now(timezone.utc) - self.registration_date).days

    @hybrid_property
    def discount_expires_days(self):
        return (self.promo_valid_to - self.promo_valid_from).days

    def __init__(self, username):
        self.username = username


Base.metadata.create_all(engine)
