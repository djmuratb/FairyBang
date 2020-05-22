#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from src import SUPPORT_MAIL
from src.messages import *

from src.core.common import bot
from src.core.utils.botutils import BotUtils

from src.core.callbackqueries.main import MainCBQ
from src.core.callbackqueries.common import common_handler, process_change_country_step, create_main_catalog_keyboard

from src.models import User


@bot.message_handler(regexp='Каталог')
def catalog(message):
    # TODO: выводить общее кол-во доступных анкет
    username, chat_id, message_id, msg_text = BotUtils.get_message_data(message)
    catalog_profiles_num = BotUtils.get_obj(User, {'username': username}).catalog_profiles_num

    kb = create_main_catalog_keyboard(catalog_profiles_num)
    bot.send_message(chat_id, MSG_CATALOG, parse_mode='Markdown', reply_markup=kb)


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
    if user.enter_promocode:
        text = MSG_DISCOUNTS.format(user.enter_promocode, str(user.promo_discount) + ' %', user.discount_expires_days)
    else:
        text = MSG_DISCOUNTS.format('не введен', 'отсутствует', 0)

    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=KB_PROMOCODE)


@bot.message_handler(regexp='Статистика')
def statistic(message):
    # TODO: вывести общее кол-во доступных в боте анкет.
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


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    username, chat_id, message_id, msg_text = BotUtils.get_message_data(call, callback=True)
    default_args = (username, chat_id, message_id)

    print('--- CALLBACK DATA --- ', msg_text)

    # --- CATALOG / FILTERS patterns
    pattern_common = re.compile(r'filters|catalog')
    pattern_option = re.compile(r'(filters|catalog):\w+:option')
    pattern_option_move = re.compile(r'(filters|catalog):\w+:option:move_(next|prev)')

    # - ch == change -
    pattern_change_country_option_value = re.compile(r'filters:country')
    pattern_change_enum_option_value = re.compile(r'ch:\w+:\w+:\w+')
    pattern_change_enum_move_back = re.compile(r'ch:back:\w+')

    # --- WELCOME ---
    if msg_text.startswith('main_country'):
        country = msg_text.split(':')[-1]
        process_change_country_step(country, username, chat_id)

    # --- DISCOUNTS / enter promocode ---
    elif msg_text.startswith('promocode'):
        MainCBQ.enter_promocode(chat_id)

    # --- CATALOG ---
    elif msg_text.startswith('main_profiles_num'):
        try:
            new_val = msg_text.split(':')[1]
        except IndexError:
            new_val = None

        MainCBQ.set_catalog_profiles_num(*default_args, new_val)

    # --- CATALOG / FILTERS (COMMON) ---
    elif re.search(pattern_change_country_option_value, msg_text):
        country = msg_text.split(':')[-1]
        MainCBQ.change_country_option_value(country, *default_args[:2])

    elif re.search(pattern_option_move, msg_text):
        msg_data = msg_text.split(':')
        common_name, filter_name = msg_data[:2]
        move_where = msg_data[-1].split('_')[1]

        increment = 1 if move_where == 'next' else -1
        common_handler(common_name, filter_name, *default_args, increment=increment)

    elif re.search(pattern_option, msg_text):
        msg_data = msg_text.split(':')
        msg_data.pop(2)
        common_name, filter_name, option_name = msg_data
        MainCBQ.options_handler(common_name, filter_name, option_name, *default_args)

    elif re.search(pattern_common, msg_text):
        common_name, common_val = msg_text.split(':')
        common_handler(common_name, common_val, *default_args)

    elif re.search(pattern_change_enum_move_back, msg_text):
        filter_name = msg_text.split(':')[-1]
        common_handler('filters', filter_name, *default_args)

    elif re.search(pattern_change_enum_option_value, msg_text):
        filter_name, option_key, option_value = msg_text.split(':')[1:]
        MainCBQ.change_enum_option_value(filter_name, option_key, option_value, *default_args)


def main_loop():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling()


if __name__ == '__main__':
    main_loop()
