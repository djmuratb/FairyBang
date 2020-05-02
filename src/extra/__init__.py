# -*- coding: utf-8 -*-
from src.extra import utils

CONFIG = utils.load_config('extra/config.yaml')

ADMIN_USERNAME                  = CONFIG['admin username']
API_TOKEN                       = CONFIG['api token']
DB_ENGINE                       = CONFIG['db engine']
ENABLE_TOR                      = CONFIG['enable tor']
DEBUG                           = CONFIG['debug']
AVAILABLE_COUNTRIES_LIST        = CONFIG['countries']
PROMOCODES                      = utils.merge_list_of_dicts(CONFIG['promocodes'])
