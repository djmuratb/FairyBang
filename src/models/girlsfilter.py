# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# from .common import Base, engine
from src.models.common import Base, engine


class GirlsFilter(Base):
    __tablename__ = 'girls_filter'

    id            = Column(Integer, primary_key=True)

    #       --- location ---
    country       = Column(String(30), name='Страна')
    city          = Column(String(50), name='Город')
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
    user_id     = Column(Integer, ForeignKey('user.id'))
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
    user_id     = Column(Integer, ForeignKey('user.id'))
    user        = relationship('User', back_populates='extended_girls_filter')
    
    def __init__(self):
        pass


class Services(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)

    #           --- sex ---
    anal                        = Column(Boolean, name='Анальный', nullable=True)
    group                       = Column(Boolean, name='Групповой', nullable=True)
    double_penetration          = Column(Boolean, name='Двойное проникновение', nullable=True)
    toys                        = Column(Boolean, name='Игрушки', nullable=True)
    classic                     = Column(Boolean, name='Классический', nullable=True)
    oral                        = Column(Boolean, name='Оральный', nullable=True)
    fetish_footfetish           = Column(Boolean, name='Фетиш/Футфетиш', nullable=True)

    #           --- affection ---
    anilingus                   = Column(Boolean, name='Анилингус', nullable=True)
    deep_blowjob                = Column(Boolean, name='Глупокий минет', nullable=True)
    kuni                        = Column(Boolean, name='Кунилингус', nullable=True)
    mbr                         = Column(Boolean, name='Минет без резинки', nullable=True)
    blowjob_auto                = Column(Boolean, name='Минет в авто', nullable=True)
    blowjob_condome             = Column(Boolean, name='Минет в резинке', nullable=True)

    #           --- massage ---
    vetka_sakuri                = Column(Boolean, name='Ветка сакуры', nullable=True)
    four_hands                  = Column(Boolean, name='В четыре руки', nullable=True)
    massage_with_continuation   = Column(Boolean, name='Массаж с продолжением', nullable=True)
    pro_massage                 = Column(Boolean, name='Профессиональный массаж', nullable=True)
    relax_massage               = Column(Boolean, name='Расслабляющий массаж', nullable=True)
    sex_and_massage_for_men     = Column(Boolean, name='Секс и массаж для мужчин', nullable=True)
    tai_massage                 = Column(Boolean, name='Тайский массаж', nullable=True)
    private_masseuses           = Column(Boolean, name='Приватные массажистки', nullable=True)
    ero_massage                 = Column(Boolean, name='Эротический массаж', nullable=True)

    #           --- strip ---
    lesbi                       = Column(Boolean, name='Лесби', nullable=True)
    strip                       = Column(Boolean, name='Стриптиз', nullable=True)

    #           --- final ---
    into_mouth                  = Column(Boolean, name='Окончание в рот', nullable=True)
    on_chest                    = Column(Boolean, name='Окончание на грудь', nullable=True)
    on_face                     = Column(Boolean, name='Окончание на лицо', nullable=True)

    #           --- bdsm ---
    bdsm                        = Column(Boolean, nullable=True)
    in_stocks                   = Column(Boolean, nullable=True)
    mrs                         = Column(Boolean, name='Госпожа', nullable=True)
    mistress_sparking           = Column(Boolean, name='Госпожа порка', nullable=True)
    easy_domination             = Column(Boolean, name='Легкое доминирование', nullable=True)
    slave_girl                  = Column(Boolean, name='Рабыня', nullable=True)
    role_playing_games          = Column(Boolean, name='Ролевые игры', nullable=True)
    sado_mazo                   = Column(Boolean, name='Садо-Мазо', nullable=True)
    strapon                     = Column(Boolean, name='Страпон', nullable=True)

    #           --- fisting ---
    anal_f                      = Column(Boolean, name='Анальный фистинг', nullable=True)
    classic_f                   = Column(Boolean, name='Классический фистинг', nullable=True)
    extreme_f                   = Column(Boolean, name='Экстрим фистинг', nullable=True)

    #           --- additional ---
    for_family                  = Column(Boolean, name='Есть молодой человек для семейной пары', nullable=True)
    copro                       = Column(Boolean, name='Копро', nullable=True)
    pip_show                    = Column(Boolean, name='Пип-Шоу', nullable=True)
    shower                      = Column(Boolean, name='Помывка в душе', nullable=True)
    rimming                     = Column(Boolean, name='Римминг', nullable=True)
    for_family2                 = Column(Boolean, name='Семейным парам', nullable=True)
    belly_dance                 = Column(Boolean, name='Танец живота', nullable=True)
    photo                       = Column(Boolean, name='Фотосъемка', nullable=True)
    escort                      = Column(Boolean, name='Эскорт', nullable=True)

    #           --- gold rain ---
    gr_output                   = Column(Boolean, name='Золотой дождь выдача', nullable=True)
    gr_input                    = Column(Boolean, name='Золотой дождь прием', nullable=True)

    #           --- relationship ---
    user_id     = Column(Integer, ForeignKey('user.id'))
    user        = relationship('User', back_populates='services')

    def __init__(self):
        pass


Base.metadata.create_all(engine)
