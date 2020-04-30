# -*- coding: utf-8 -*-
from src.extra import utils

CONFIG = utils.load_config('extra/config.yaml')

API_TOKEN = CONFIG['api token']
DB_ENGINE = CONFIG['db engine']
AVAILABLE_COUNTRIES_LIST = CONFIG['countries']
PROMOCODES = utils.merge_list_of_dicts(CONFIG['promocodes'])
