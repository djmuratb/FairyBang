# -*- coding: utf-8 -*-
from src.core.common import bot
from src.core.utils.botutils import Keyboards

from src.core.callbackqueries.filters import FiltersCBQ
from src.core.callbackqueries.catalog import CatalogCBQ


COMMON_CLASSES = {'filters': FiltersCBQ, 'catalog': CatalogCBQ}


def common_handler(common_name, filter_name, username, chat_id, message_id, increment=0):
    args = (filter_name, username, chat_id, increment)
    kb_options = COMMON_CLASSES.get(common_name)(*args).get_keyboard_options()

    prefix = f'{common_name}:{filter_name}:option:'
    keyboard = Keyboards.create_inline_keyboard_ext(*kb_options, prefix=prefix, row_width=1)
    bot.edit_message_text(f'🅰️ *{filter_name}*', chat_id, message_id, parse_mode='Markdown', reply_markup=keyboard)
