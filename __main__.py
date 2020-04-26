# -*- coding: utf-8 -*-
import telebot

import utils

from telebot import types

from text import *


# TODO: admin panel
# TODO: notifications
# TODO: statistic of bought girls and spend money since register moment.
# TODO: added logging (require for payments and promo codes payments)

# AFTER SLEEPING STEP
# - make settings (change: country, town, enter: promo code)
# - make yaml config and get data from it


CONFIG = utils.load_config('config.yaml')
API_TOKEN = CONFIG['api token']
AVAILABLE_COUNTRIES_LIST = CONFIG['countries']

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


class GirlsFilter:
    pass


class User:
    def __init__(self):
        self.city = None
        self.town = None


def create_reply_keyboard(*buttons, resize_keyboard=True, row_width=2):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=row_width)
    markup.add(*(telebot.types.KeyboardButton(button) for button in buttons))
    return markup


def create_inline_keyboard(*buttons, cb_prefix='cb_', row_width=2):
    markup = types.InlineKeyboardMarkup(row_width)
    markup.add(*(types.InlineKeyboardButton(button, callback_data=f'{cb_prefix}{button}') for button in buttons))
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome = WELCOME.format(message.from_user.username)
    keyboard = create_inline_keyboard(*AVAILABLE_COUNTRIES_LIST, row_width=1)

    bot.send_message(message.chat.id, welcome, parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, '🌍 Выберите Вашу страну из списка доступных стран', reply_markup=keyboard)


def process_city_step(message):
    if message.text in AVAILABLE_CITIES_LIST:
        menu_keyboard = create_reply_keyboard(*MENU_ITEMS)
        bot.send_message(message.chat.id, MENU_WELCOME, reply_markup=menu_keyboard)
    elif message.text == '/reset':
        msg = bot.send_message(message.chat.id, '⭕ Хотите начать сначала? Введите что нибудь')
        bot.register_next_step_handler(msg, send_welcome)
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


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    cb_text = call.message.json['reply_markup']['inline_keyboard'][0][0]['text']

    if cb_text in AVAILABLE_COUNTRIES_LIST:
        msg = bot.send_message(call.message.chat.id, '🏢 Введите название города, в котором Вам требуется девушка')
        bot.register_next_step_handler(msg, process_city_step)


def main_loop():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling()


if __name__ == '__main__':
    main_loop()
