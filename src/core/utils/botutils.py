# -*- coding: utf-8 -*-
from typing import Sequence
from collections import namedtuple

from telebot import types

from src.models import session, User, GirlsFilter, ExtendedGirlsFilter, Services


class Keyboards:
    @staticmethod
    def create_reply_keyboard(*buttons: Sequence[str], resize_keyboard: bool = True, row_width: int = 2):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=row_width)
        markup.add(*(types.KeyboardButton(button) for button in buttons))
        return markup

    @staticmethod
    def create_inline_keyboard(*buttons: Sequence[str], prefix: str = 'cb_', postfix: str = '', row_width: int = 2):
        markup = types.InlineKeyboardMarkup(row_width)
        markup.add(
            *(
                types.InlineKeyboardButton(button, callback_data=f'{prefix}{button}{postfix}')
                for button in buttons
            )
        )
        return markup

    @staticmethod
    def create_inline_keyboard_ext(*options: namedtuple, prefix: str = 'cb_', row_width: int = 1):
        markup = types.InlineKeyboardMarkup(row_width)
        markup.add(
            *(
                types.InlineKeyboardButton(option.name, callback_data=f'{prefix}{option.callback}')
                for option in options
            )
        )
        return markup


class BotUtils:
    @staticmethod
    def get_obj(class_or_instance, filter_by: dict):
        if isinstance(class_or_instance, type) and filter_by:
            class_or_instance = session.query(class_or_instance).filter_by(**filter_by).one()

        return class_or_instance

    @staticmethod
    def write_changes(class_or_instance: object or type, attr=None, value=None, only_commit=True, filter_by: dict = None):
        # TODO: check update method
        obj = BotUtils.get_obj(class_or_instance, filter_by)
        if attr and value is not None:
            obj.__setattr__(attr, value)

        if not only_commit:
            session.add(obj)

        session.commit()

    @staticmethod
    def create_user(username):
        user = session.query(User).filter_by(username=username).first()
        if not user:
            user = User(username)
            user.girls_filter = GirlsFilter()
            user.extended_girls_filter = ExtendedGirlsFilter()
            user.services = Services()
            BotUtils.write_changes(user, only_commit=False)

        return user

    @staticmethod
    def get_message_data(obj, callback=False):
        """
        :param obj: message or call object
        :param callback: if param is callback query data
        :return: username, chat_id, message_id, text of object.
        """
        if callback:
            data = (obj.message.chat.username, obj.message.chat.id, obj.message.message_id, obj.data)
        else:
            data = (obj.chat.username, obj.chat.id, obj.message_id, obj.text)

        return data
