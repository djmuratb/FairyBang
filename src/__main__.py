#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot

from datetime import datetime

from telebot import types, apihelper
from sqlalchemy.orm import lazyload

from src.models import User, GirlsFilter, ExtendedGirlsFilter, Services, session
from src.extra import utils, API_TOKEN, ENABLE_TOR, AVAILABLE_COUNTRIES_LIST, PROMOCODES
from src.extra.text import *


if ENABLE_TOR:
    apihelper.proxy = {'https':'socks5h://127.0.0.1:9050'}

bot = telebot.TeleBot(API_TOKEN)
user_dict = {}
state = {}


class Utils:
    @staticmethod
    def write_changes(obj, attr=None, value=None, only_commit=True):
        if attr and value:
            obj.__setattr__(attr, value)

        if not only_commit:
            session.add(obj)

        session.commit()

    @staticmethod
    def create_user(username, chat_id):
        user = session.query(User).filter_by(username=username).first()
        if not user:
            user = User(username)
            user.girls_filter = GirlsFilter()
            user.extended_girls_filter = ExtendedGirlsFilter()
            user.services = Services()
            Utils.write_changes(user, only_commit=False)

        user_dict[chat_id] = user
        return user


@bot.message_handler(commands=['start'])
def process_welcome_step(message):
    Utils.create_user(message.from_user.username, message.chat.id)

    welcome = MSG_WELCOME.format(message.from_user.username)
    keyboard = utils.create_inline_keyboard(*AVAILABLE_COUNTRIES_LIST, row_width=1)

    bot.send_message(message.chat.id, welcome, parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, MSG_ENTER_COUNTRY, parse_mode='Markdown', reply_markup=keyboard)


def process_city_step(message):
    city = message.text.capitalize()

    if city in AVAILABLE_CITIES_LIST:
        Utils.write_changes(user_dict[message.chat.id].girls_filter, 'city', city)
        bot.send_message(message.chat.id, MSG_MENU_ATTENTION, parse_mode='Markdown', reply_markup=KB_MENU)
    elif message.text == '/reset':
        msg = bot.send_message(message.chat.id, MSG_RESET, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_welcome_step)
    else:
        msg = bot.send_message(message.chat.id, MSG_UNAVAILABLE_CITY, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_city_step)


def process_promocode_step(message):
    promocode = message.text
    if promocode in PROMOCODES.values():
        bot.send_message(message.chat.id, MSG_SUCCESS_PROMO, parse_mode='Markdown', reply_markup=KB_MENU)
    elif promocode.endswith('Отмена'):
        bot.send_message(message.chat.id, MSG_CANCELED, parse_mode='Markdown', reply_markup=KB_MENU)
    else:
        msg = bot.send_message(message.chat.id, MSG_ERROR_PROMO, parse_mode='Markdown', reply_markup=KB_CANCEL)
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
    bot.send_message(message.chat.id, MSG_DISCOUNTS, parse_mode='Markdown', reply_markup=KB_PROMOCODE)


@bot.message_handler(regexp='Статистика')
def statistic(message):
    user = Utils.create_user(message.from_user.username, message.chat.id)
    msg = MSG_STATISTIC.format(
        0,
        0,
        0,

        utils.get_delta_days_from_dates(user.registration_date),
        user.total_txs,
        int(user.total_qiwi_sum),
        user.total_girls,
    )
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')


class CallbackQueryUtils:
    @staticmethod
    def get_girls_options(user_instance, msg_data):
        filters = {
            'Базовый': user_instance.girls_filter,
            'Расширенный': user_instance.extended_girls_filter,
            'Услуги': user_instance.services
        }

        filter = filters.get(msg_data.split(' ')[0])
        return {
            column.name: getattr(user_instance.girls_filter, column.key)
            for column in user_instance.girls_filter.__table__.columns
            if column.name not in ('id', 'user_id')
        }


class CallbackQuery:
    @staticmethod
    def cb_countries(country_name, chat_id, username):
        Utils.write_changes(user_dict[chat_id].girls_filter, 'country', country_name)
        msg = bot.send_message(chat_id, MSG_ENTER_CITY, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_city_step)

    @staticmethod
    def cb_promocode(chat_id, message_id):
        msg = bot.edit_message_text(MSG_ENTER_PROMO, chat_id, message_id, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_promocode_step)

    @staticmethod
    def filters_handler(username, msg_data, chat_id, message_id):
        user = session.query(User).filter_by(username=username).one()
        girls_options = CallbackQueryUtils.get_girls_options(user, msg_data)
        print(girls_options)
        go = utils.chunk_dict(girls_options, 4)

        for el in go:
            print(el)

        # keyboard = utils.create_inline_keyboard(*lst[0])
        # bot.edit_message_text('some msg', chat_id, message_id, parse_mode='Markdown', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    msg_data = call.data.split('_')[1]
    if msg_data in AVAILABLE_COUNTRIES_LIST:
        CallbackQuery.cb_countries(msg_data, call.message.chat.id, call.message.from_user.username)
    elif 'PROMOCODE' in msg_data:
        CallbackQuery.cb_promocode(call.message.chat.id, call.message.message_id)
    elif msg_data in FILTERS_ITEMS:
        CallbackQuery.filters_handler(call.message.chat.username, msg_data, call.message.chat.id, call.message.message_id)


def main_loop():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling()


if __name__ == '__main__':
    main_loop()
