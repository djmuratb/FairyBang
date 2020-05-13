# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

from src.models.common import Base, engine, Common
from src.models.enums import *


class GirlsFilter(Common):
    __tablename__ = 'girls_filter'

    id            = Column(Integer, primary_key=True)

    #       --- location ---
    country       = Column(String(30), name='Страна', default='🇷🇺 Россия', key='country')
    city          = Column(String(50), name='Город', default='Москва', key='city')
    subway        = Column(Enum(Subway, values_callable=lambda obj: [e.value for e in obj]), name='Район', default=Subway.two.value, key='subway')

    #       --- appearance details ---
    age           = Column(ARRAY(Integer, as_tuple=True), name='Возраст', default=(18, 80), key='age')
    height        = Column(ARRAY(Integer, as_tuple=True), name='Рост', default=(140, 200), key='height')
    chest         = Column(ARRAY(Integer, as_tuple=True), name='Грудь', default=(1, 12), key='chest')

    #       --- price ---
    price         = Column(ARRAY(Integer, as_tuple=True), name='Цена', default=(1_000, 20_000), key='price')

    #       --- relationship ---
    user_username   = Column(String(50), ForeignKey('user.username', ondelete='CASCADE'))
    user            = relationship('User', back_populates='girls_filter')

    def __init__(self):
        pass


class ExtendedGirlsFilter(Common):
    __tablename__ = 'extended_girls_filter'

    id                          = Column(Integer, primary_key=True)

    #       --- additional appearance ---
    category                    = Column(String(30), name='Категория', key='category')
    hair_color                  = Column(String(20), name='Цвет волос', key='hair_color')
    body_type                   = Column(String(20), name='Телосложение', key='body_type')
    skin_color                  = Column(String(20), name='Цвет кожи', key='skin_color')
    nationality                 = Column(String(30), name='Национальность', key='nationality')

    #       --- other ---
    smoking                     = Column(Boolean, name='Курение', key='smoking')
    girl_friends                = Column(Boolean, name='Подружки', key='girl_friends')

    #       --- prices ---
    app_one_hour                = Column(ARRAY(Integer, as_tuple=True), name='Апартаменты 1 час', key='app_one_hour')
    app_two_hours               = Column(ARRAY(Integer, as_tuple=True), name='Апартаменты 2 часа', key='app_two_hours')
    departure_to_you            = Column(ARRAY(Integer, as_tuple=True), name='Выезд к Вам', key='departure_to_you')
    departure_to_you_night      = Column(ARRAY(Integer, as_tuple=True), name='Выезд к Вам на ночь', key='departure_to_you_night')

    #       --- relationship ---
    user_username   = Column(String(50), ForeignKey('user.username', ondelete='CASCADE'))
    user            = relationship('User', back_populates='extended_girls_filter')
    
    def __init__(self):
        pass


Base.metadata.create_all(engine)
