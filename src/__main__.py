#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from src import SUPPORT_MAIL
from src.core.callbackquery import MainCBQ
from src.core.common import bot
from src.core.utils.botutils import BotUtils
from src.messages import *


@bot.message_handler(regexp='Каталог')
def catalog(message):
    print(000, message.text)


@bot.message_handler(regexp='Фильтры')
def filters(message):
    bot.send_message(message.chat.id, MSG_FILTERS, parse_mode='Markdown', reply_markup=KB_FILTERS_MENU)


@bot.message_handler(regexp='Гарантии|О сервисе')
def about(message):
    abouts = {'Гарантии': MSG_GUARANTY, 'О сервисе': MSG_ABOUT_SERVICE.format(SUPPORT_MAIL)}
    about_text = abouts.get(' '.join(message.text.split()[1:]))
    bot.send_message(message.chat.id, about_text, parse_mode='Markdown')


@bot.message_handler(regexp='Скидки')
def discounts(message):
    username, chat_id, message_id, msg_text = BotUtils.get_message_data(message)
    user = BotUtils.create_user(username=username)
    if user.promocode:
        text = MSG_DISCOUNTS.format(user.promocode, str(user.promo_discount) + ' %', user.discount_expires_days)
    else:
        text = MSG_DISCOUNTS.format('не введен', 'отсутствует', 0)

    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=KB_PROMOCODE)


@bot.message_handler(regexp='Статистика')
def statistic(message):
    username, chat_id, message_id, msg_text = BotUtils.get_message_data(message)
    user = BotUtils.create_user(username)
    msg = MSG_STATISTIC.format(
        0,
        0,
        0,

        user.days_since_register,
        user.total_txs,
        int(user.total_qiwi_sum),
        user.total_girls,
    )
    bot.send_message(chat_id, msg, parse_mode='Markdown')


@bot.message_handler(regexp='Отмена')
def cancel(message):
    bot.send_message(message.chat.id, MSG_CANCELED, reply_markup=KB_MENU)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    username, chat_id, message_id, msg_text = BotUtils.get_message_data(call, callback=True)

    print('--- CALLBACK DATA --- ', msg_text)

    # --- CATALOG / FILTERS patterns
    pattern_common = re.compile(r'filters|catalog')
    pattern_option = re.compile(r'(filters|catalog):\w+:option')
    pattern_option_move = re.compile(r'(filters|catalog):\w+:option:move_(next|prev)')

    # --- WELCOME ---
    if msg_text.startswith('main_country'):
        country = msg_text.split(':')[-1]
        MainCBQ.countries(country, username, chat_id)

    # --- DISCOUNTS / enter promocode ---
    elif msg_text.startswith('promocode'):
        MainCBQ.promocode(chat_id, message_id)

    # --- CATALOG / FILTERS ---
    elif re.search(pattern_option_move, msg_text):
        msg_data = msg_text.split(':')
        common_name, filter_name = msg_data[:2]
        move_where = msg_data[-1].split('_')[1]

        increment = 1 if move_where == 'next' else -1
        MainCBQ.common_handler(common_name, filter_name, username, chat_id, message_id, increment=increment)

    elif re.search(pattern_option, msg_text):
        msg_data = msg_text.split(':')
        msg_data.pop(2)
        common_name, filter_name, option_name = msg_data
        MainCBQ.options_handler(common_name, filter_name, option_name, username, chat_id, message_id)

    elif re.search(pattern_common, msg_text):
        common_name, common_val = msg_text.split(':')
        MainCBQ.common_handler(common_name, common_val, username, chat_id, message_id)


def main_loop():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling()


if __name__ == '__main__':
    main_loop()
