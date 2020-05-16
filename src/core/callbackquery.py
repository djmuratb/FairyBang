# -*- coding: utf-8 -*-
import itertools
import collections as cs

from abc import ABCMeta, abstractmethod

from sqlalchemy import inspect, Column, ARRAY, Enum

from src.core.common import bot
from src.core.stepsprocesses import process_city_step, process_promocode_step, process_change_range_option_val_step

from src.core.utils import pyutils
from src.core.utils.botutils import BotUtils, Keyboards
from src.core.utils.validators import VALIDATORS

from src.models import session, Services, FILTERS
from src.messages import *


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

    def __init__(self, query_name, username, chat_id, increment=0):
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
        filter_ = FILTERS.get(self._query_name)
        return filter_.as_list(
            session.query(filter_).filter(filter_.user_username == self._username).one()
        )

    def get_chunk_girls_options(self):
        girls_options = self.get_girls_options()
        return pyutils.chunk_list(girls_options, self._chunk_size)

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
    _msg0 = 'Введите диапазон значений.'
    _msg1 = 'Введите значение от *{}* до *{}*.'
    _msg2 = 'Выберите один из вариантов.'
    _msg3 = 'Введите следующее значение: *{}*.'

    Option = cs.namedtuple('Option', ['name', 'callback'])

    def __init__(self, filter_name, option_name_key, username, chat_id, message_id):
        self._filter_name = filter_name
        self._option_name_key = option_name_key
        self._username = username
        self._chat_id = chat_id
        self._message_id = message_id

        self._filter_class = FILTERS.get(self._filter_name)

    def add_move_back_option(self, options):
        move_cb = f'ch:back:{self._filter_name}'
        return itertools.chain(options, (self.Option(name='⬅️ Назад', callback=move_cb),))

    def get_options(self, default_values, option_key):
        options = (
            self.Option(name=val, callback=f'ch:{self._filter_name}:{option_key}:{val}')
            for val in default_values
        )
        return self.add_move_back_option(options)

    def send_enum_msg(self, msg, default_values, option_key):
        options = self.get_options(default_values, option_key)
        kb = Keyboards.create_inline_keyboard_ext(*options, prefix='', row_width=2)
        bot.edit_message_text(msg, self._chat_id, self._message_id, parse_mode='Markdown', reply_markup=kb)

    def send_range_msg(self, msg, default_values, value_type, key):
        chat_msg = bot.send_message(self._chat_id, msg, parse_mode='Markdown', reply_markup=KB_CANCEL)
        bot.register_next_step_handler(
            chat_msg,
            process_change_range_option_val_step,
            default_values=default_values,
            value_type=value_type,
            filter_class=self._filter_class,
            key=key,
        )

    @staticmethod
    def get_msg_value_from_column(column: Column):
        column_type = column.__dict__['type']

        if isinstance(column_type, ARRAY):
            try:
                data = (column.default.arg, 'range')
            except AttributeError:
                data = (None, 'range')
        elif isinstance(column_type, Enum):
            data = (column.type.enums, 'enum')
        else:
            data = ('', 'location')

        return data

    def get_msg_data_from_column(self, column: Column):
        value, value_type = self.get_msg_value_from_column(column)
        if value_type == 'range':
            if value:
                text = self._msg1.format(*value) + MSG_HELP_RANGE
            else:
                text = self._msg0 + MSG_HELP_RANGE
        elif value_type == 'enum':
            text = self._msg2
        else:
            text = self._msg3.format(column.name)

        return text, value, value_type, column.key

    def get_msg_data(self):
        columns = inspect(self._filter_class).columns
        msg = value_type = default_values = key = None

        for col in columns:
            if col.key == self._option_name_key:
                msg, default_values, value_type, key = self.get_msg_data_from_column(col)
                msg = MSG_CHANGE_OPTION_VAL.format(msg)

        return msg, default_values, value_type, key

    def send_change_option_value_msg(self):
        if isinstance(self._filter_class, Services):
            # TODO: change value of service option
            return

        msg, default_values, value_type, key = self.get_msg_data()

        if value_type == 'range':
            self.send_range_msg(msg, default_values, value_type, key)
        elif value_type == 'enum':
            self.send_enum_msg(msg, default_values, key)
        elif value_type == 'location':
            # TODO: country / city / Subway process step
            pass


class MainCBQ:
    @staticmethod
    def countries(country_name, username, chat_id):
        user = BotUtils.create_user(username)
        BotUtils.write_changes(user.girls_filter, 'country', country_name)

        msg = bot.send_message(chat_id, MSG_ENTER_CITY, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_city_step)

    @staticmethod
    def promocode(chat_id):
        msg = bot.send_message(chat_id, MSG_ENTER_PROMO, parse_mode='Markdown', reply_markup=KB_CANCEL)
        bot.register_next_step_handler(msg, process_promocode_step)

    @staticmethod
    def change_enum_option_value(filter_name, option_key, value, username, chat_id, message_id):
        filter_class = FILTERS.get(filter_name)
        is_valid = VALIDATORS.get('enum').validate(enum_key=option_key, value=value)

        if is_valid:
            obj = session.query(filter_class).filter_by(user_username=username).one()
            BotUtils.write_changes(obj, option_key, value)

        MainCBQ.common_handler('filters', filter_name, username, chat_id, message_id)

    @staticmethod
    def options_handler(common_name, filter_name, option_name, username, chat_id, message_id):
        args = (filter_name, option_name, username, chat_id, message_id)
        if common_name == 'filters':
            FiltersOptionsHandler(*args).send_change_option_value_msg()
        elif common_name == 'catalog':
            pass

    @staticmethod
    def common_handler(common_name, filter_name, username, chat_id, message_id, increment=0):
        args = (filter_name, username, chat_id, increment)
        common_classes = {'filters': FiltersCBQ, 'catalog': CatalogCBQ}
        kb_options = common_classes.get(common_name)(*args).get_keyboard_options()

        prefix = f'{common_name}:{filter_name}:option:'
        keyboard = Keyboards.create_inline_keyboard_ext(*kb_options, prefix=prefix, row_width=1)
        bot.edit_message_text(f'🅰️ *{filter_name}*', chat_id, message_id, parse_mode='Markdown', reply_markup=keyboard)
