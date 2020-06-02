# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property

from src.models.common import BaseUser, engine_user, UserBase
from src.models.mixins import BaseFilterMixin, ExtFilterMixin, ServicesMixin


csc = 'all,delete,delete-orphan'


class UserGirlServices(ServicesMixin, UserBase):
    __tablename__ = 'users_girl_services'

    #           --- relationship ---
    user_username   = Column(String(50), ForeignKey('users.username', ondelete='CASCADE'))
    user            = relationship('User', back_populates='services')

    def __init__(self):
        pass


class UserGirlExtFilter(ExtFilterMixin, UserBase):
    __tablename__ = 'users_girl_ext_filter'

    #       --- prices ---
    app_one_hour            = Column(ARRAY(Integer, as_tuple=True), name='Апартаменты 1 час', key='app_one_hour')
    app_two_hours           = Column(ARRAY(Integer, as_tuple=True), name='Апартаменты 2 часа', key='app_two_hours')
    departure_to_you        = Column(ARRAY(Integer, as_tuple=True), name='Выезд к Вам', key='departure_to_you')
    departure_to_you_night  = Column(ARRAY(Integer, as_tuple=True), name='Выезд к Вам на ночь', key='departure_to_you_night')

    #       --- relationship ---
    user_username   = Column(String(50), ForeignKey('users.username', ondelete='CASCADE'))
    user            = relationship('User', back_populates='ext_filter')

    def __init__(self):
        pass


class UserGirlBaseFilter(BaseFilterMixin, UserBase):
    __tablename__ = 'users_girl_base_filter'

    #       --- appearance details ---
    age             = Column(ARRAY(Integer, as_tuple=True), name='Возраст', default=(18, 80), key='age')
    height          = Column(ARRAY(Integer, as_tuple=True), name='Рост', default=(140, 200), key='height')
    chest           = Column(ARRAY(Integer, as_tuple=True), name='Грудь', default=(1, 12), key='chest')

    #       --- price ---
    price           = Column(ARRAY(Integer, as_tuple=True), name='Цена', default=(1_000, 20_000), key='price')

    #       --- relationship ---
    user_username   = Column(String(50), ForeignKey('users.username', ondelete='CASCADE'))
    user            = relationship('User', back_populates='base_filter')

    def __init__(self):
        pass


class User(UserBase):
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

    #       --- relationship ---
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


BaseUser.metadata.create_all(engine_user)
