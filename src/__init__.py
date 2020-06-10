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


# --- MAIN OPTIONS ---
ADMIN_USERNAME                  = CONFIG['admin username']
API_TOKEN                       = CONFIG['api token']

DATABASES                       = CONFIG['databases']
USERS_DB                        = DATABASES['user']
GIRLS_DB                        = DATABASES['girls']

# --- WEBHOOKS ---
WEBHOOK_HOST                    = CONFIG['webhook host']
WEBHOOK_PORT                    = CONFIG['webhook port']
WEBHOOK_LISTEN                  = CONFIG['webhook listen']

WEBHOOK_SSL_CERT                = CONFIG['webhook ssl cert']
WEBHOOK_SSL_PRIV                = CONFIG['webhook ssl priv']

WEBHOOK_URL_BASE                = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH                = "/{}/".format(API_TOKEN)

# --- REQUIRE LISTS ---
AVAILABLE_COUNTRIES_LIST        = CONFIG['countries']
PROMOCODES                      = CONFIG['promocodes']
QIWI_WALLETS                    = CONFIG['qiwi wallets']

# --- OTHER OPTIONS ---
SUPPORT_MAIL                    = CONFIG['mail']
ENABLE_TOR                      = CONFIG['enable tor']
DEBUG                           = CONFIG['debug']
