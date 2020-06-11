# -*- coding: utf-8 -*-
from src.models.common import user_session, girl_session
from src.models.user import User, UserGirlBaseFilter, UserGirlExtFilter, UserGirlServices
from src.models.girl import Girl, GirlBaseFilter, GirlExtFilter, GirlServices
from src.models.admin import Admin


FILTERS = {
    'base_filter'   : UserGirlBaseFilter,
    'ext_filter'    : UserGirlExtFilter,
    'services'      : UserGirlServices,
}
