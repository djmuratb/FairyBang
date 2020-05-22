# -*- coding: utf-8 -*-
from src.messages import *

from src.core.common import bot
from src.core.types import Option
from src.core.stepsprocesses import process_change_city_step

from src.core.utils.botutils import BotUtils, Keyboards

from src.core.callbackqueries.filters import FiltersCBQ
from src.core.callbackqueries.catalog import CatalogCBQ


COMMON_CLASSES = {'filters': FiltersCBQ, 'catalog': CatalogCBQ}


def common_handler(common_name, filter_name, username, chat_id, message_id, increment=0):
    args = (filter_name, username, chat_id, increment)
    kb_options = COMMON_CLASSES.get(common_name)(*args).get_keyboard_options()

    prefix = f'{common_name}:{filter_name}:option:'
    keyboard = Keyboards.create_inline_keyboard_ext(*kb_options, prefix=prefix, row_width=1)
    bot.edit_message_text(f'🅰️ *{filter_name}*', chat_id, message_id, parse_mode='Markdown', reply_markup=keyboard)


def process_change_country_step(country_name, username, chat_id):
    user = BotUtils.create_user(username)
    BotUtils.write_changes(user.girls_filter, 'country', country_name)

    msg = bot.send_message(chat_id, MSG_ENTER_CITY, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_change_city_step)


def create_main_catalog_keyboard(catalog_profiles_num):
    buttons = (
        (f'⚙️ ПОКАЗЫВАТЬ ПО   -   {catalog_profiles_num}', 'main_profiles_num'),
        ('👠 ПОКАЗАТЬ АНКЕТЫ', 'catalog')
    )
    options = (Option(name=name, callback=callback) for name, callback in buttons)
    return Keyboards.create_inline_keyboard_ext(*options, prefix='', row_width=1)
