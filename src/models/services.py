# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.models.common import Base, engine, Common


class Services(Common):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)

    #           --- sex ---
    anal                        = Column(Boolean, name='Анальный', nullable=True, key='anal')
    group                       = Column(Boolean, name='Групповой', nullable=True, key='group')
    double_penetration          = Column(Boolean, name='Двойное проникновение', nullable=True, key='double_penetration')
    toys                        = Column(Boolean, name='Игрушки', nullable=True, key='toys')
    classic                     = Column(Boolean, name='Классический', nullable=True, key='classic')
    oral                        = Column(Boolean, name='Оральный', nullable=True, key='oral')
    fetish_footfetish           = Column(Boolean, name='Фетиш/Футфетиш', nullable=True, key='fetish_footfetish')

    #           --- affection ---
    anilingus                   = Column(Boolean, name='Анилингус', nullable=True, key='anilingus')
    deep_blowjob                = Column(Boolean, name='Глупокий минет', nullable=True, key='deep_blowjob')
    kuni                        = Column(Boolean, name='Кунилингус', nullable=True, key='kuni')
    mbr                         = Column(Boolean, name='Минет без резинки', nullable=True, key='mbr')
    blowjob_auto                = Column(Boolean, name='Минет в авто', nullable=True, key='blowjob_auto')
    blowjob_condome             = Column(Boolean, name='Минет в резинке', nullable=True, key='blowjob_condome')

    #           --- massage ---
    vetka_sakuri                = Column(Boolean, name='Ветка сакуры', nullable=True, key='vetka_sakuri')
    four_hands                  = Column(Boolean, name='В четыре руки', nullable=True, key='four_hands')
    massage_with_continuation   = Column(Boolean, name='Массаж с продолжением', nullable=True, key='massage_with_continuation')
    pro_massage                 = Column(Boolean, name='Профессиональный массаж', nullable=True, key='pro_massage')
    relax_massage               = Column(Boolean, name='Расслабляющий массаж', nullable=True, key='relax_massage')
    sex_and_massage_for_men     = Column(Boolean, name='Секс и массаж для мужчин', nullable=True, key='sex_and_massage_for_men')
    tai_massage                 = Column(Boolean, name='Тайский массаж', nullable=True, key='tai_massage')
    private_masseuses           = Column(Boolean, name='Приватные массажистки', nullable=True, key='private_masseuses')
    ero_massage                 = Column(Boolean, name='Эротический массаж', nullable=True, key='ero_massage')

    #           --- strip ---
    lesbi                       = Column(Boolean, name='Лесби', nullable=True, key='lesbi')
    strip                       = Column(Boolean, name='Стриптиз', nullable=True, key='strip')

    #           --- final ---
    into_mouth                  = Column(Boolean, name='Окончание в рот', nullable=True, key='into_mouth')
    on_chest                    = Column(Boolean, name='Окончание на грудь', nullable=True, key='on_chest')
    on_face                     = Column(Boolean, name='Окончание на лицо', nullable=True, key='on_face')

    #           --- bdsm ---
    bdsm                        = Column(Boolean, nullable=True, name='БДСМ', key='bdsm')
    in_stocks                   = Column(Boolean, nullable=True, name='В чулках', key='in_stocks')
    mrs                         = Column(Boolean, name='Госпожа', nullable=True, key='mrs')
    mistress_sparking           = Column(Boolean, name='Госпожа порка', nullable=True, key='mistress_sparking')
    easy_domination             = Column(Boolean, name='Легкое доминирование', nullable=True, key='easy_domination')
    slave_girl                  = Column(Boolean, name='Рабыня', nullable=True, key='slave_girl')
    role_playing_games          = Column(Boolean, name='Ролевые игры', nullable=True, key='role_playing_games')
    sado_mazo                   = Column(Boolean, name='Садо-Мазо', nullable=True, key='sado_mazo')
    strapon                     = Column(Boolean, name='Страпон', nullable=True, key='strapon')

    #           --- fisting ---
    anal_f                      = Column(Boolean, name='Анальный фистинг', nullable=True, key='anal_f')
    classic_f                   = Column(Boolean, name='Классический фистинг', nullable=True, key='classic_f')
    extreme_f                   = Column(Boolean, name='Экстрим фистинг', nullable=True, key='extreme_f')

    #           --- additional ---
    for_family                  = Column(Boolean, name='+ МЧ семейной паре', nullable=True, key='for_family')
    copro                       = Column(Boolean, name='Копро', nullable=True, key='copro')
    pip_show                    = Column(Boolean, name='Пип-Шоу', nullable=True, key='pip_show')
    shower                      = Column(Boolean, name='Помывка в душе', nullable=True, key='shower')
    rimming                     = Column(Boolean, name='Римминг', nullable=True, key='rimming')
    for_family2                 = Column(Boolean, name='Семейным парам', nullable=True, key='for_family2')
    belly_dance                 = Column(Boolean, name='Танец живота', nullable=True, key='belly_dance')
    photo                       = Column(Boolean, name='Фотосъемка', nullable=True, key='photo')
    escort                      = Column(Boolean, name='Эскорт', nullable=True, key='escort')

    #           --- gold rain ---
    gr_output                   = Column(Boolean, name='Золотой дождь выдача', nullable=True, key='gr_output')
    gr_input                    = Column(Boolean, name='Золотой дождь прием', nullable=True, key='gr_input')

    #           --- relationship ---
    user_username   = Column(String, ForeignKey('user.username', ondelete='CASCADE'))
    user            = relationship('User', back_populates='services')

    def __init__(self):
        pass


Base.metadata.create_all(engine)
