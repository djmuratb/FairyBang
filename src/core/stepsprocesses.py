# -*- coding: utf-8 -*-
from telebot import types

from src.core.common import bot
from src.core.utils.botutils import BotUtils
from src.extra import AVAILABLE_COUNTRIES_LIST, PROMOCODES
from src.messages import *


@bot.message_handler(commands=['start'])
def start(message):
    username, chat_id, message_id, msg_text = BotUtils.get_message_data(message)
    BotUtils.create_user(username)

    welcome = MSG_WELCOME.format(username)
    keyboard = pyutils.create_inline_keyboard(*AVAILABLE_COUNTRIES_LIST, prefix='main_country:', row_width=1)

    bot.send_message(chat_id, welcome, parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(chat_id, MSG_ENTER_COUNTRY, parse_mode='Markdown', reply_markup=keyboard)


def process_city_step(message):
    username, chat_id, message_id, msg_text = BotUtils.get_message_data(message)
    city = msg_text.capitalize()

    if city in AVAILABLE_CITIES_LIST:
        BotUtils.write_changes(BotUtils.create_user(username).girls_filter, 'city', city)
        bot.send_message(chat_id, MSG_MENU_ATTENTION, parse_mode='Markdown', reply_markup=KB_MENU)
    elif msg_text == '/reset':
        msg = bot.send_message(chat_id, MSG_RESET, parse_mode='Markdown')
        bot.register_next_step_handler(msg, start)
    else:
        msg = bot.send_message(chat_id, MSG_UNAVAILABLE_CITY, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_city_step)


def process_promocode_step(message):
    username, chat_id, message_id, promocode = BotUtils.get_message_data(message)
    promocode_data = PROMOCODES.get(promocode, None)

    if promocode_data:
        user = BotUtils.create_user(username)
        user.promocode = promocode
        pyutils.set_attrs_values_from_dict(promocode_data, user, date_specific=True)

        BotUtils.write_changes(user)
        bot.send_message(chat_id, MSG_SUCCESS_PROMO, parse_mode='Markdown', reply_markup=KB_MENU)

    elif promocode.endswith('Отмена'):
        bot.send_message(chat_id, MSG_CANCELED, parse_mode='Markdown', reply_markup=KB_MENU)

    else:
        msg = bot.send_message(chat_id, MSG_ERROR_PROMO, parse_mode='Markdown', reply_markup=KB_CANCEL)
        bot.register_next_step_handler(msg, process_promocode_step)


def change_option_value_handler(message, **kwargs):
    # TODO: write validator
    pass
