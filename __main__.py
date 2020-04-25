# -*- coding: utf-8 -*-
import telebot
from telebot import types

from text import *


API_TOKEN = '917583816:AAG-Jf82LgKFrEFS_ECgbjF7VYVpGwOOjdo'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


class ValueChecker:
    @staticmethod
    def is_available_value(value, iterable):
        if value in iterable:
            return True

        return False


class GirlsFilter:
    pass


class User:
    def __init__(self, country, town):
        self.city = country
        self.town = town


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
    msg = bot.send_message(message.chat.id, WELCOME.format(message.from_user.username),
                           parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_country_step)


def process_country_step(message):
    pass


def process_menu_step(message):
    menu_keyboard = create_keyboard(*MENU_ITEMS)
    bot.send_message(message.chat.id, 'Menu text', reply_markup=menu_keyboard)


def main_loop():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling()


if __name__ == '__main__':
    main_loop()
