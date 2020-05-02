# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.models.common import Base, engine


class GirlsFilter(Base):
    __tablename__ = 'girls_filter'

    id            = Column(Integer, primary_key=True)

    #       --- location ---
    country       = Column(String(30), name='Страна', default='🇷🇺 Россия', key='country')
    city          = Column(String(50), name='Город', default='Москва', key='city')
    subway        = Column(String(50), name='Район', nullable=True, key='subway')

    #       --- appearance details ---
    age_min       = Column(Integer, name='Возраст от', default=18, key='age_min')
    age_max       = Column(Integer, name='Возраст до', default=80, key='age_max')
    height_min    = Column(Integer, name='Рост от', default=140, key='height_min')
    height_max    = Column(Integer, name='Рост до', default=200, key='height_max')
    chest_min     = Column(Integer, name='Грудь от', default=1, key='chest_min')
    chest_max     = Column(Integer, name='Грудь до', default=12, key='chest_max')

    #       --- price ---
    price_min     = Column(Integer, name='Цена от', default=1_000, key='price_min')
    price_max     = Column(Integer, name='Цена до', default=20_000, key='price_max')

    #       --- relationship ---
    user_id     = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user        = relationship('User', back_populates='girls_filter')

    def __init__(self):
        pass


class ExtendedGirlsFilter(Base):
    __tablename__ = 'extended_girls_filter'

    id                          = Column(Integer, primary_key=True)

    #       --- additional appearance ---
    hair_color                  = Column(String(20), name='Цвет волос', key='hair_color')
    body_type                   = Column(String(20), name='Телосложение', key='body_type')
    skin_color                  = Column(String(20), name='Цвет кожи', key='skin_color')
    nationality                 = Column(String(30), name='Национальность', key='nationality')

    #       --- other ---
    smoking                     = Column(Boolean, name='Курение', key='smoking')
    girl_friends                = Column(Boolean, name='Подружки', key='girl_friends')

    #       --- prices ---
    apartments_one_hour_min     = Column(Integer, name='Апартаменты 1 час от', key='apartments_one_hour_min')
    apartments_one_hour_max     = Column(Integer, name='Апартаменты 1 час до', key='apartments_one_hour_max')
    apartments_two_hours_min    = Column(Integer, name='Апартаменты 2 часа от', key='apartments_two_hours_min')
    apartments_two_hours_max    = Column(Integer, name='Апартаменты 2 часа до', key='apartments_two_hours_max')

    departure_to_you_min        = Column(Integer, name='Выезд к Вам от', key='departure_to_you_min')
    departure_to_you_max        = Column(Integer, name='Выезд к Вам до', key='departure_to_you_max')

    departure_to_you_night_min  = Column(Integer, name='Выезд к Вам на ночь от', key='departure_to_you_night_min')
    departure_to_you_night_max  = Column(Integer, name='Выезд к Вам на ночь до', key='departure_to_you_night_max')

    #       --- relationship ---
    user_id     = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user        = relationship('User', back_populates='extended_girls_filter')
    
    def __init__(self):
        pass


Base.metadata.create_all(engine)
