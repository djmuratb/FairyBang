# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

from src.models.common import Base, engine, Common
from src.models.extra.enums import *


class GirlsFilter(Common):
    __tablename__ = 'girls_filter'

    id            = Column(Integer, primary_key=True)

    #       --- location ---
    country       = Column(String(30), name='Страна', default='🇷🇺 Россия', key='country')
    city          = Column(String(50), name='Город', default='Москва', key='city')
    subway        = Column(String(50), name='Район', nullable=True, key='subway')

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
    category                    = Column(Enum(ExtCategory, values_callable=Common.values_callable, name='Категория'),
                                         name='Категория', default=ExtCategory.not_important.value, key='category')
    hair_color                  = Column(Enum(ExtHairColor, values_callable=Common.values_callable, name='Цвет волос'),
                                         name='Цвет волос', default=ExtHairColor.not_important.value, key='hair_color')
    body_type                   = Column(Enum(ExtBodyType, values_callable=Common.values_callable, name='Телосложение'),
                                         name='Телосложение', default=ExtBodyType.not_important.value, key='body_type')
    skin_color                  = Column(Enum(ExtSkinColor, values_callable=Common.values_callable, name='Цвет кожи'),
                                         name='Цвет кожи', default=ExtSkinColor.not_important.value, key='skin_color')
    nationality                 = Column(Enum(ExtNationality, values_callable=Common.values_callable,
                                              name='Национальность'), name='Национальность',
                                         default=ExtNationality.not_important.value, key='nationality')

    #       --- other ---
    smoking                     = Column(Enum(ExtSmoking, values_callable=Common.values_callable, name='Курение'),
                                         name='Курение', default=ExtSmoking.not_important.value, key='smoking')
    girl_friends                = Column(Enum(ExtGirlFriends, values_callable=Common.values_callable, name='Подружки'),
                                         name='Подружки', default=ExtGirlFriends.not_important.value, key='girl_friends')

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
