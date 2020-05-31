# -*- coding: utf-8 -*-
from src.messages import *
from src.models import user_session, User

from src.core.helpers.types import Option
from src.core.common import bot
from src.core.helpers.botutils import BotUtils
from src.core.callbackqueries.base import BaseCBQ


def create_main_catalog_keyboard(catalog_profiles_num):
    buttons = (
        (f'⚙️ ПОКАЗЫВАТЬ ПО   -   {catalog_profiles_num}', f'{PX_CAT_SET}profiles_num'),
        ('👠 ПОКАЗАТЬ АНКЕТЫ', PX_CAT)
    )
    options = (Option(name=name, callback=callback) for name, callback in buttons)
    return Keyboards.create_inline_keyboard_ext(*options, prefix='', row_width=1)


def set_catalog_num_profiles_per_page(username, chat_id, message_id, new_val):
    def is_valid(val):
        return (val == 1 or val % 5 == 0) and val != 0

    if new_val:
        user = user_session.query(User).filter_by(username=username).one()
        BotUtils.write_changes(user, 'catalog_profiles_num', new_val)

        kb = create_main_catalog_keyboard(user.catalog_profiles_num)
        bot.edit_message_text(MSG_CATALOG, chat_id, message_id, parse_mode='Markdown', reply_markup=kb)
        bot.send_message(chat_id, MSG_SUCCESS_CHANGE_OPTION, parse_mode='Markdown')
    else:
        options = (Option(name=f'{x}', callback=f'{PX_CAT_SET}profiles_num:{x}') for x in range(11) if is_valid(x))
        kb = Keyboards.create_inline_keyboard_ext(*options, prefix='', row_width=1)
        bot.edit_message_text(MSG_CATALOG_NUM_PROFILES, chat_id, message_id, parse_mode='Markdown', reply_markup=kb)


class CatalogCBQ(BaseCBQ):
    __slots__ = ('_query_name', '_username', '_chat_id', '_increment')

    def __init__(self, query_name, username, chat_id, increment=0):
        self._query_name = query_name
        self._username = username
        self._chat_id = chat_id
        self._increment = increment

    def get_keyboard_options(self):
        return []

    def send_message(self):
        from src.core.common import bot

        file = '/home/cyberpunk/Pictures/dadzai.jpg'
        # photo = open(file, 'rb')

        for _ in range(7):
            photo = open(file, 'rb')
            bot.send_photo(self._chat_id, photo, reply_markup=KB_FILTERS_MENU)
