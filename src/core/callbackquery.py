# -*- coding: utf-8 -*-
import itertools
import collections as cs

from abc import ABCMeta, abstractmethod

from sqlalchemy import inspect, Column

from src.core.stepsprocess import process_city_step, process_promocode_step
from src.core.common import bot
from src.core.botutils import BotUtils
from src.models import session, GirlsFilter, ExtendedGirlsFilter, Services
from src.extra.text import *


filters_state = {}


class BaseCBQ(metaclass=ABCMeta):
    Option = cs.namedtuple('Option', ['name', 'callback'])
    move_options_data = (('⬅️ Предыдущая', 'move_previous'), ('➡️️ Следующая', 'move_next'))

    @abstractmethod
    def get_keyboard_options(self):
        pass


class CatalogCBQ(BaseCBQ):
    __slots__ = ('_query_name', '_username', '_chat_id', '_increment')

    def __init__(self, query_name, username, chat_id, increment):
        self._query_name = query_name
        self._username = username
        self._chat_id = chat_id
        self._increment = increment

    def get_keyboard_options(self):
        return []


class FiltersCBQ(BaseCBQ):
    __slots__ = ('_query_name', '_username', '_chat_id', '_increment')

    _chunk_size = 7

    def __init__(self, query_name, username, chat_id, increment):
        self._query_name     = query_name
        self._username       = username
        self._chat_id        = chat_id
        self._increment      = increment

        self._state          = None
        self._add_move       = True

    @staticmethod
    def get_max_size_name_of_all_options(all_options):
        return len(
            max(
                (map(lambda x: ''.join(x[1:]), all_options))
            )
        )

    def get_option_name_with_indent(self, all_options, name_data):
        max_str_size = self.get_max_size_name_of_all_options(all_options)
        str_size = len(''.join(name_data))
        whs_num = 1 if max_str_size - str_size == 0 else max_str_size - str_size
        whs = ' ' * int(whs_num * 2.3777 + 35)
        option_name = whs.join(name_data)
        return option_name

    def get_girls_options(self):
        filters = {'Базовый': GirlsFilter, 'Расширенный': ExtendedGirlsFilter, 'Услуги': Services}
        filter_ = filters.get(self._query_name)
        return filter_.as_list(
            session.query(filter_).filter(filter_.user_username == self._username).one()
        )

    def get_chunk_girls_options(self):
        girls_options = self.get_girls_options()
        return utils.chunk_list(girls_options, self._chunk_size)

    def get_part_from_chunk_girls_options(self):
        chunk_girls_options = self.get_chunk_girls_options()
        state = filters_state.get(self._chat_id, 0) + self._increment
        if state == len(chunk_girls_options):
            state = 0

        if len(chunk_girls_options) == 1:
            self._add_move = False

        filters_state[self._chat_id] = self._state = state
        return chunk_girls_options[state]

    def get_options_objects(self):
        part_girls_options = self.get_part_from_chunk_girls_options()
        return (
            self.Option(name=self.get_option_name_with_indent(part_girls_options, data), callback=key)
            for key, *data in part_girls_options
        )

    def add_move_options(self):
        options_objects = self.get_options_objects()

        if not self._add_move:
            return options_objects

        if self._state == 0:
            move_options = (self.move_options_data[1], )
        else:
            move_options = self.move_options_data

        move_options = (self.Option(name, callback) for name, callback in move_options)
        return itertools.chain(options_objects, move_options)

    def get_keyboard_options(self):
        return self.add_move_options()


class FiltersOptionsHandler:
    _filters = {'Базовый': GirlsFilter, 'Расширенный': ExtendedGirlsFilter, 'Услуги': Services}

    _msg1 = 'Введите значение от {} до {}.'
    _msg2 = 'Введите один из представленных варинатов: {}.'
    _msg3 = 'Введите следующее значение: {}.'

    def __init__(self, filter_name, option_name_key, username, chat_id):
        self._filter_name = filter_name
        self._option_name_key = option_name_key
        self._username = username
        self._chat_id = chat_id

        self._filter = self._filters.get(self._filter_name)

    def get_msg_text(self, column: Column):
        try:
            data = column.type.enums
        except AttributeError:
            data = column.default.arg

        if len(data) == 2:
            msg = self._msg1.format(*data)
        elif isinstance(data, list):
            msg = self._msg2.format(', '.join(column.type.enums))
        else:
            msg = self._msg3.format(column.name)

        return msg

    def foo(self):
        # FIXME: fix ext filter and services.
        columns = inspect(self._filter).columns
        msg = None

        for col in columns:
            if col.key == self._option_name_key:
                msg = self.get_msg_text(col)

        print(msg)


class MainCBQ:
    @staticmethod
    def countries(country_name, username, chat_id):
        user = BotUtils.create_user(username)
        BotUtils.write_changes(user.girls_filter, 'country', country_name)

        msg = bot.send_message(chat_id, MSG_ENTER_CITY, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_city_step)

    @staticmethod
    def promocode(chat_id, message_id):
        msg = bot.edit_message_text(MSG_ENTER_PROMO, chat_id, message_id, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_promocode_step)

    @staticmethod
    def options_handler(common_name, filter_name, option_name, username, chat_id, message_id, increment=0):
        # args = (filter_name, option_name, username, chat_id, increment)
        # FiltersOptions(*args).foo()

        args = (filter_name, option_name, username, chat_id)
        FiltersOptionsHandler(*args).foo()

    @staticmethod
    def common_handler(common_name, filter_name, username, chat_id, message_id, increment=0):
        args = (filter_name, username, chat_id, increment)
        common_classes = {'filters': FiltersCBQ, 'catalog': CatalogCBQ}
        kb_options = common_classes.get(common_name)(*args).get_keyboard_options()

        prefix = f'{common_name}:{filter_name}:option:'
        keyboard = utils.create_inline_keyboard_ext(*kb_options, prefix=prefix, row_width=1)
        bot.edit_message_text(f'🅰️ *{filter_name}*', chat_id, message_id, parse_mode='Markdown', reply_markup=keyboard)
