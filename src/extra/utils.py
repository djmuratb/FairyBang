# -*- coding: utf-8 -*-
import os
import yaml

from datetime import datetime
from collections import ChainMap
from itertools import islice
from typing import Sequence

from telebot import types


def create_reply_keyboard(*buttons: Sequence[str], resize_keyboard: bool = True, row_width: int = 2):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=row_width)
    markup.add(*(types.KeyboardButton(button) for button in buttons))
    return markup


def create_inline_keyboard(*buttons: Sequence[str], prefix: str ='cb_', postfix: str = '', row_width: int = 2):
    markup = types.InlineKeyboardMarkup(row_width)
    markup.add(
        *(
            types.InlineKeyboardButton(button, callback_data=f'{prefix}{button}{postfix}')
            for button in buttons
        )
    )
    return markup


def create_inline_keyboard_ext(*options: Sequence[str], prefix: str ='cb_', postfix: str = '', row_width: int = 1):
    markup = types.InlineKeyboardMarkup(row_width)
    markup.add(
        *(
            types.InlineKeyboardButton(option.name, callback_data=f'{prefix}{option.callback}')
            for option in options
        )
    )
    return markup



def get_abs_path(file: str):
    return os.path.join(
        os.getcwd(), file
    )


def load_config(cfg: str):
    path = get_abs_path(cfg)
    with open(path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def merge_list_of_dicts(lst: list):
    return dict(ChainMap(*lst))


def get_delta_days_from_dates(first: datetime, latest: datetime = datetime.now()):
    return (latest - first).days


def chunk_dict(data: dict, parts_num: int):
    it = iter(data)
    return [
        {key: data[key] for key in islice(it, parts_num)} for i in range(0, len(data), parts_num)
    ]


def chunk_list(data: list, parts_num: int):
    it = iter(data)
    return [
        [d for d in islice(it, parts_num)] for i in range(0, len(data), parts_num)
    ]
