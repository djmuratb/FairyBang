# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.models.common import Base, engine


class GirlsFilter(Base):
    __tablename__ = 'girls_filter'

    id            = Column(Integer, primary_key=True)

    #       --- location ---
    country       = Column(String(30), name='Страна', default='🇷🇺 Россия')
    city          = Column(String(50), name='Город', default='Москва')
    subway        = Column(String(50), name='Район', nullable=True)

    #       --- appearance details ---
    age_min       = Column(Integer, name='Возраст от', default=18)
    age_max       = Column(Integer, name='Возраст до', default=80)
    height_min    = Column(Integer, name='Рост от', default=140)
    height_max    = Column(Integer, name='Рост до', default=200)
    chest_min     = Column(Integer, name='Грудь от', default=1)
    chest_max     = Column(Integer, name='Грудь до', default=12)

    #       --- price ---
    price_min     = Column(Integer, name='Цена от', default=1_000)
    price_max     = Column(Integer, name='Цена до', default=20_000)

    #       --- relationship ---
    user_id     = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user        = relationship('User', back_populates='girls_filter')

    def __init__(self):
        pass


class ExtendedGirlsFilter(Base):
    __tablename__ = 'extended_girls_filter'

    id                          = Column(Integer, primary_key=True)

    #       --- additional appearance ---
    hair_color                  = Column(String(20), name='Цвет волос')
    body_type                   = Column(String(20), name='Телосложение')
    skin_color                  = Column(String(20), name='Цвет кожи')
    nationality                 = Column(String(30), name='Национальность')

    #       --- other ---
    smoking                     = Column(Boolean, name='Курение')
    girl_friends                = Column(Boolean, name='Подружки')

    #       --- prices ---
    apartments_one_hour_min     = Column(Integer, name='Апартаменты 1 час от')
    apartments_one_hour_max     = Column(Integer, name='Апартаменты 1 час до')
    apartments_two_hours_min    = Column(Integer, name='Апартаменты 2 часа от')
    apartments_two_hours_max    = Column(Integer, name='Апартаменты 2 часа до')

    departure_to_you_min        = Column(Integer, name='Выезд к Вам от')
    departure_to_you_max        = Column(Integer, name='Выезд к Вам до')

    departure_to_you_night_min  = Column(Integer, name='Выезд к Вам на ночь от')
    departure_to_you_night_max  = Column(Integer, name='Выезд к Вам на ночь до')

    #       --- relationship ---
    user_id     = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user        = relationship('User', back_populates='extended_girls_filter')
    
    def __init__(self):
        pass


Base.metadata.create_all(engine)
