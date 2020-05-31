# -*- coding: utf-8 -*-
from src.models.common import session
from src.models.user import User, UserGirlBaseFilter, UserGirlExtFilter, UserGirlServices
from src.models.admin import Admin


FILTERS = {
    'Базовый'       : UserGirlBaseFilter,
    'Расширенный'   : UserGirlExtFilter,
    'Услуги'        : UserGirlServices,
}
