# -*- coding: utf-8 -*-
from src.core.utils import pyutils

CONFIG = pyutils.load_config('config.yaml')

ADMIN_USERNAME                  = CONFIG['admin username']
API_TOKEN                       = CONFIG['api token']
SUPPORT_MAIL                    = CONFIG['mail']
ENABLE_TOR                      = CONFIG['enable tor']
DEBUG                           = CONFIG['debug']

DATABASES                       = CONFIG['databases']
MAIN_DB                         = DATABASES['main']
GIRLS_DB                        = DATABASES['girls']

AVAILABLE_COUNTRIES_LIST        = CONFIG['countries']
PROMOCODES                      = CONFIG['promocodes']
