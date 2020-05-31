# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, LargeBinary

from src.models.common import Common
from src.models.base import BaseFilter, ExtFilter, Services


csc = 'all,delete,delete-orphan'


class GirlServices(Services):
    pass


class GirlExtFilter(ExtFilter):
    pass


class GirlBaseFilter(BaseFilter):
    pass


class Girl(Common):
    __tablename__ = 'girls'

    id              = Column(Integer, primary_key=True)

    #       --- main ---
    name            = Column(String(50), name='О себе', nullable=False, key='name')
    about           = Column(String(500), name='О себе', nullable=True, key='about')

    #       --- photo ---
    preview_photo   = Column(LargeBinary, nullable=False)
    photo1          = Column(LargeBinary, nullable=True)
    photo2          = Column(LargeBinary, nullable=True)
    photo3          = Column(LargeBinary, nullable=True)

    #       --- contacts ---
    phone           = Column(String(30), nullable=False)
    viber           = Column(String(30), nullable=True)
    whatsapp        = Column(String(30), nullable=True)
    telegram        = Column(String(30), nullable=True)
