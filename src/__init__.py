# -*- coding: utf-8 -*-
import sys

from src.core.helpers import pyutils


try:
    cfg_path = sys.argv[1]
except IndexError:
    cfg_path = 'config.yaml'

try:
    CONFIG = pyutils.load_config(cfg_path)
except FileNotFoundError:
    raise Exception('Incorrect configuration file path entered.')

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
