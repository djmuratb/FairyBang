# -*- coding: utf-8 -*-
from src import utils


CONFIG = utils.load_config('config.yaml')
API_TOKEN = CONFIG['api token']
DB_ENGINE = CONFIG['db engine']
AVAILABLE_COUNTRIES_LIST = CONFIG['countries']
PROMOCODES = CONFIG['promocodes']
