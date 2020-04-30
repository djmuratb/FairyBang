# -*- coding: utf-8 -*-
import os
import yaml

from collections import ChainMap

from telebot import types


def create_reply_keyboard(*buttons, resize_keyboard=True, row_width=2):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=row_width)
    markup.add(*(types.KeyboardButton(button) for button in buttons))
    return markup


def create_inline_keyboard(*buttons, cb_prefix='cb_', row_width=2):
    markup = types.InlineKeyboardMarkup(row_width)
    markup.add(*(types.InlineKeyboardButton(button, callback_data=f'{cb_prefix}{button}') for button in buttons))
    return markup


def get_abs_path(file):
    return os.path.join(
        os.getcwd(), file
    )


def load_config(cfg):
    path = get_abs_path(cfg)

    with open(path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def merge_list_of_dicts(lst):
    return dict(ChainMap(*lst))


def get_delta_days_from_dates(first, latest):
    return (latest - first).days
