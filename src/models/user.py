# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.common import Base, engine


class User(Base):
    __tablename__ = 'user'

    id            = Column(Integer, primary_key=True)
    username      = Column(String(55), unique=True)

    girls_filter            = relationship('GirlsFilter', uselist=False, back_populates='user')
    extended_girls_filter   = relationship('ExtendedGirlsFilter', uselist=False, back_populates='user')
    services                = relationship('Services', uselist=False, back_populates='user')

    def __init__(self, username):
        self.username = username


Base.metadata.create_all(engine)
