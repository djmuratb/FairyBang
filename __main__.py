# -*- coding: utf-8 -*-
import re

import telebot
from telebot import types

from text import *


API_TOKEN = '917583816:AAG-Jf82LgKFrEFS_ECgbjF7VYVpGwOOjdo'

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
    bot.send_message(message.chat.id, 'Выберите Вашу страну из списка доступных стран', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    cb_text = call.message.json['reply_markup']['inline_keyboard'][0][0]['text']

    if cb_text in AVAILABLE_COUNTRIES_LIST:
        msg = bot.send_message(call.message.chat.id, 'Введите название города, в котором Вам нужна проститутка')
        bot.register_next_step_handler(msg, process_city_step)


def process_city_step(message):
    if message.text in AVAILABLE_CITIES_LIST:
        menu_keyboard = create_reply_keyboard(*MENU_ITEMS)
        msg = bot.send_message(message.chat.id, MENU_WELCOME, reply_markup=menu_keyboard)
        bot.register_next_step_handler(msg, process_menu_step)
    elif message.text == '/reset':
        msg = bot.send_message(message.chat.id, 'Хотите начать сначала? Введите что нибудь')
        bot.register_next_step_handler(msg, send_welcome)

    else:
        msg = bot.send_message(message.chat.id, UNAVAILABLE_CITY)
        bot.register_next_step_handler(msg, process_city_step)


def process_menu_step(message):
    pass


def main_loop():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling()


if __name__ == '__main__':
    main_loop()
