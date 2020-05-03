# -*- coding: utf-8 -*-
from src.extra import utils

CONFIG = utils.load_config('extra/config.yaml')

ADMIN_USERNAME                  = CONFIG['admin username']
API_TOKEN                       = CONFIG['api token']
DATABASE                        = CONFIG['database']
ENABLE_TOR                      = CONFIG['enable tor']
DEBUG                           = CONFIG['debug']

AVAILABLE_COUNTRIES_LIST        = CONFIG['countries']
PROMOCODES                      = CONFIG['promocodes']
