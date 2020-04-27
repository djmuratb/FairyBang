#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot

from telebot import types

from src import CONFIG, utils
from src.text import *
from src.models import User, GirlsFilter, ExtendedGirlsFilter, session


# TODO: admin panel
# TODO: notifications
# TODO: statistic of bought girls and spend money since register moment.
# TODO: added logging (require for payments and promo codes payments)

# AFTER SLEEPING STEP
# - make settings (change: country, town, enter: promo code)


API_TOKEN = CONFIG['api token']
AVAILABLE_COUNTRIES_LIST = CONFIG['countries']

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def process_welcome_step(message):
    welcome = WELCOME.format(message.from_user.username)
    keyboard = utils.create_inline_keyboard(*AVAILABLE_COUNTRIES_LIST, row_width=1)

    bot.send_message(message.chat.id, welcome, parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, '🌍 Выберите Вашу страну из списка доступных стран', reply_markup=keyboard)


def process_city_step(message):
    if message.text in AVAILABLE_CITIES_LIST:
        menu_keyboard = utils.create_reply_keyboard(*MENU_ITEMS)
        bot.send_message(message.chat.id, MENU_WELCOME, reply_markup=menu_keyboard)
    elif message.text == '/reset':
        msg = bot.send_message(message.chat.id, '⭕ Хотите начать сначала? Введите что нибудь')
        bot.register_next_step_handler(msg, process_welcome_step)
    else:
        msg = bot.send_message(message.chat.id, UNAVAILABLE_CITY)
        bot.register_next_step_handler(msg, process_city_step)


@bot.message_handler(regexp='Каталог')
def catalog(message):
    print(000, message.text)


@bot.message_handler(regexp='Фильтры')
def filters(message):
    print(000, message.text)


@bot.message_handler(regexp='Гарантии|Скидки|О сервисе')
def about(message):
    abouts = {'Гарантии': GUARANTY, 'Скидки': DISCOUNTS, 'О сервисе': ABOUT_SERVICE}
    about_text = abouts.get(' '.join(message.text.split()[1:]))
    bot.send_message(message.chat.id, about_text)


@bot.message_handler(regexp='Настройки')
def settings(message):
    print(333, message.text)


class CallbackQuery:
    @staticmethod
    def cb_countries(chat_id):
        msg = bot.send_message(chat_id, '🏢 Введите название города, в котором Вам требуется девушка')
        bot.register_next_step_handler(msg, process_city_step)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    cb_text = call.message.json['reply_markup']['inline_keyboard'][0][0]['text']

    if cb_text in AVAILABLE_COUNTRIES_LIST:
        CallbackQuery.cb_countries(call.message.chat.id)


def main_loop():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling()


if __name__ == '__main__':
    main_loop()
