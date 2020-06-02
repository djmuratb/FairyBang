# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Enum

from src.models.common import Common
from src.models.extra.enums import *


class BaseFilterMixin:
    id            = Column(Integer, primary_key=True)

    #       --- location ---
    country       = Column(String(30), name='Страна', default='🇷🇺 Россия', key='country')
    city          = Column(String(50), name='Город', default='Москва', key='city')
    subway        = Column(String(50), name='Район', nullable=True, key='subway')


class ExtFilterMixin:
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
    nationality                 = Column(Enum(ExtNationality, values_callable=Common.values_callable, name='Национальность'),
                                         name='Национальность', default=ExtNationality.not_important.value, key='nationality')

    #       --- other ---
    smoking                     = Column(Enum(ExtSmoking, values_callable=Common.values_callable, name='Курение'),
                                         name='Курение', default=ExtSmoking.not_important.value, key='smoking')
    girl_friends                = Column(Enum(ExtGirlFriends, values_callable=Common.values_callable, name='Подружки'),
                                         name='Подружки', default=ExtGirlFriends.not_important.value, key='girl_friends')
