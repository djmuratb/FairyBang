#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import itertools
import functools
import collections as cs

import telebot

from datetime import datetime

from telebot import types, apihelper
from sqlalchemy.orm import lazyload

from src.models import User, GirlsFilter, ExtendedGirlsFilter, Services, session
from src.extra import utils, API_TOKEN, ENABLE_TOR, AVAILABLE_COUNTRIES_LIST, PROMOCODES
from src.extra.text import *


if ENABLE_TOR:
    apihelper.proxy = {'https': 'socks5h://127.0.0.1:9050'}

bot = telebot.TeleBot(API_TOKEN)
filters_state = {}


class Utils:
    @staticmethod
    def write_changes(obj, attr=None, value=None, only_commit=True):
        if attr and value:
            obj.__setattr__(attr, value)

        if not only_commit:
            session.add(obj)

        session.commit()

    @staticmethod
    def create_user(username, chat_id, updated=False):
        user = session.query(User).filter_by(username=username).first()
        if not user:
            user = User(username)
            user.girls_filter = GirlsFilter()
            user.extended_girls_filter = ExtendedGirlsFilter()
            user.services = Services()
            Utils.write_changes(user, only_commit=False)

        return user

    @staticmethod
    def get_message_data(obj, callback=False):
        """
        :param obj: message or call object
        :return: username, chat_id, message_id, text of object.
        """
        if callback:
            data = (obj.message.chat.username, obj.message.chat.id, obj.message.message_id, obj.data)
        else:
            data = (obj.chat.username, obj.chat.id, obj.message_id, obj.text)

        return data


@bot.message_handler(commands=['start'])
def process_welcome_step(message):
    username, chat_id, message_id, msg_text = Utils.get_message_data(message)
    Utils.create_user(username, chat_id)

    welcome = MSG_WELCOME.format(username)
    keyboard = utils.create_inline_keyboard(*AVAILABLE_COUNTRIES_LIST, prefix='main_country_', row_width=1)

    bot.send_message(chat_id, welcome, parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(chat_id, MSG_ENTER_COUNTRY, parse_mode='Markdown', reply_markup=keyboard)


def process_city_step(message):
    username, chat_id, message_id, msg_text = Utils.get_message_data(message)
    city = msg_text.capitalize()

    if city in AVAILABLE_CITIES_LIST:
        Utils.write_changes(Utils.create_user(username, chat_id).girls_filter, 'city', city)
        bot.send_message(chat_id, MSG_MENU_ATTENTION, parse_mode='Markdown', reply_markup=KB_MENU)
    elif text == '/reset':
        msg = bot.send_message(chat_id, MSG_RESET, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_welcome_step)
    else:
        msg = bot.send_message(chat_id, MSG_UNAVAILABLE_CITY, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_city_step)


def process_promocode_step(message):
    username, chat_id, message_id, promocode = Utils.get_message_data(message)
    promocode_data = PROMOCODES.get(promocode, None)

    if promocode_data:
        user = Utils.create_user(username, chat_id, updated=True)
        user.promocode = promocode
        utils.set_attrs_values_from_dict(promocode_data, user, date_specific=True)

        Utils.write_changes(user)
        bot.send_message(chat_id, MSG_SUCCESS_PROMO, parse_mode='Markdown', reply_markup=KB_MENU)

    elif promocode.endswith('Отмена'):
        bot.send_message(chat_id, MSG_CANCELED, parse_mode='Markdown', reply_markup=KB_MENU)

    else:
        msg = bot.send_message(chat_id, MSG_ERROR_PROMO, parse_mode='Markdown', reply_markup=KB_CANCEL)
        bot.register_next_step_handler(msg, process_promocode_step)


@bot.message_handler(regexp='Каталог')
def catalog(message):
    print(000, message.text)


@bot.message_handler(regexp='Фильтры')
def filters(message):
    bot.send_message(message.chat.id, MSG_FILTERS, parse_mode='Markdown', reply_markup=KB_FILTERS_MENU)


@bot.message_handler(regexp='Гарантии|О сервисе')
def about(message):
    abouts = {'Гарантии': MSG_GUARANTY, 'О сервисе': MSG_ABOUT_SERVICE}
    about_text = abouts.get(' '.join(message.text.split()[1:]))
    bot.send_message(message.chat.id, about_text, parse_mode='Markdown')


@bot.message_handler(regexp='Скидки')
def discounts(message):
    username, chat_id, message_id, msg_text = Utils.get_message_data(message)
    user = Utils.create_user(username=username, chat_id=chat_id, updated=True)
    if user.promocode:
        discount_expires_days = utils.get_delta_days_from_dates(user.promo_valid_from, user.promo_valid_to)
        text = MSG_DISCOUNTS.format(user.promocode, user.promo_discount, discount_expires_days)
    else:
        text = MSG_DISCOUNTS.format('не введен', 'отсутствует', 0)

    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=KB_PROMOCODE)


@bot.message_handler(regexp='Статистика')
def statistic(message):
    username, chat_id, message_id, msg_text = Utils.get_message_data(message)
    user = Utils.create_user(username, chat_id)
    msg = MSG_STATISTIC.format(
        0,
        0,
        0,

        utils.get_delta_days_from_dates(user.registration_date),
        user.total_txs,
        int(user.total_qiwi_sum),
        user.total_girls,
    )
    bot.send_message(chat_id, msg, parse_mode='Markdown')


class CatalogCallbackQuery:
    def __init__(self, query_name, username, chat_id, increment):
        self._filter_name = query_name
        self._username = username
        self._chat_id = chat_id
        self._increment = increment

    def get_keyboard_options(self):
        pass


class FiltersCallbackQuery:
    Option = cs.namedtuple('Option', ['name', 'callback'])
    move_options_data = (('⬅️ Предыдущая', 'move_previous_{}'), ('➡️️ Следующая', 'move_next_{}'))

    _chunk_size = 6

    def __init__(self, query_name, username, chat_id, increment):
        self._filter_name    = query_name
        self._username       = username
        self._chat_id        = chat_id
        self._increment      = increment

        self._state          = None

    @staticmethod
    def get_max_size_name_of_all_options(all_options):
        return len(max((map(lambda x: ''.join(x[1:]), all_options))))

    def get_option_name_with_indent(self, all_options, name_data):
        max_str_size = self.get_max_size_name_of_all_options(all_options)
        str_size = len(''.join(name_data))
        whs_num = 1 if max_str_size - str_size == 0 else max_str_size - str_size
        whs = ' ' * int(whs_num * 2.3777 + 35)
        option_name = whs.join(name_data)
        return option_name

    def get_girls_options(self):
        user = session.query(User).filter_by(username=self._username).one()
        filters = {'Базовый': user.girls_filter, 'Расширенный': user.extended_girls_filter, 'Услуги': user.services}
        filter = filters.get(self._filter_name)
        return filter.as_list(filter)

    def get_chuncked_girls_options(self):
        girls_options = self.get_girls_options()
        return utils.chunk_list(girls_options, self._chunk_size)

    def get_part_from_chuncked_girls_options(self):
        chuncked_girls_options = self.get_chuncked_girls_options()
        state = filters_state.get(self._chat_id, 0) + self._increment
        if state == len(chuncked_girls_options):
            state = 0

        filters_state[self._chat_id] = self._state = state
        return chuncked_girls_options[state]

    def get_options_objects(self):
        part_gilrs_options = self.get_part_from_chuncked_girls_options()
        return (
            self.Option(name=self.get_option_name_with_indent(part_gilrs_options, data), callback=key)
            for key, *data in part_gilrs_options
        )

    def add_move_options(self):
        options_objects = self.get_options_objects()
        if self._state == 0:
            move_options = (self.move_options_data[1], )
        else:
            move_options = self.move_options_data

        move_options = (self.Option(name, callback.format(self._filter_name)) for name, callback in move_options)
        return itertools.chain(options_objects, move_options)

    def get_keyboard_options(self):
        return self.add_move_options()


class CallbackQuery:
    @staticmethod
    def cb_countries(country_name, username, chat_id):
        user = Utils.create_user(username, chat_id)
        Utils.write_changes(user.girls_filter, 'country', country_name)

        msg = bot.send_message(chat_id, MSG_ENTER_CITY, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_city_step)

    @staticmethod
    def cb_promocode(chat_id, message_id):
        msg = bot.edit_message_text(MSG_ENTER_PROMO, chat_id, message_id, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_promocode_step)

    @staticmethod
    def common_handler(common_name, filter_name, username, chat_id, message_id, increment=0):
        args = (filter_name, username, chat_id, increment)
        if common_name == 'filters':
            kb_options = FiltersCallbackQuery(*args).get_keyboard_options()
        elif common_name == 'catalog':
            kb_options = CatalogCallbackQuery(*args).get_keyboard_options()

        keyboard = utils.create_inline_keyboard_ext(*kb_options, prefix=f'{common_name}_option_', row_width=1)
        bot.edit_message_text(f'🅰️ *{filter_name}*', chat_id, message_id, parse_mode='Markdown', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    username, chat_id, message_id, msg_text = Utils.get_message_data(call, callback=True)

    print('--- CALLBACK DATA --- ', msg_text)

    # --- CATALOG / FILTERS patterns
    pattern_common = re.compile(r'filters|catalog')
    pattern_option = re.compile(r'(filters|catalog)_option')
    pattern_option_move = re.compile(r'(filters|catalog)_option_move')

    # --- WELCOME ---
    if msg_text.startswith('main_country'):
        country = msg_text.split('_')[-1]
        CallbackQuery.cb_countries(country, username, chat_id)

    # --- DISCOUNTS / enter promocde ---
    elif msg_text.startswith('promocode'):
        CallbackQuery.cb_promocode(chat_id, message_id)

    # --- CATALOG / FILTERS ---
    elif re.search(pattern_option_move, msg_text):
        msg_data = msg_text.split('_')

        common_name = msg_data[0]
        where, common_val = msg_data[-2:]
        increment = 1 if where == 'next' else -1

        CallbackQuery.common_handler(common_name, common_val, username, chat_id, message_id, increment=increment)

    elif re.search(pattern_option, msg_text):
        pass

    elif re.search(pattern_common, msg_text):
        common_name, common_val = msg_text.split('_')
        CallbackQuery.common_handler(common_name, common_val, username, chat_id, message_id)


def main_loop():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling()


if __name__ == '__main__':
    main_loop()
