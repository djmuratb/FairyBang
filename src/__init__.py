# -*- coding: utf-8 -*-
from src.core.helpers import pyutils

CONFIG = pyutils.load_config('config.yaml')

ADMIN_USERNAME                  = CONFIG['admin username']
API_TOKEN                       = CONFIG['api token']
SUPPORT_MAIL                    = CONFIG['mail']
ENABLE_TOR                      = CONFIG['enable tor']
DEBUG                           = CONFIG['debug']

DATABASES                       = CONFIG['databases']
USERS_DB                        = DATABASES['user']
GIRLS_DB                        = DATABASES['girls']

AVAILABLE_COUNTRIES_LIST        = CONFIG['countries']
PROMOCODES                      = CONFIG['promocodes']
QIWI_WALLETS                    = CONFIG['qiwi wallets']
