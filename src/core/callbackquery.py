# -*- coding: utf-8 -*-
import itertools
import collections as cs

from abc import ABCMeta, abstractmethod

from src.core.stepsprocess import process_city_step, process_promocode_step
from src.core.common import bot
from src.core.botutils import BotUtils
from src.models import session, User
from src.extra.text import *


filters_state = {}


class BaseCBQ(metaclass=ABCMeta):
    Option = cs.namedtuple('Option', ['name', 'callback'])
    move_options_data = (('⬅️ Предыдущая', 'move_previous_{}'), ('➡️️ Следующая', 'move_next_{}'))

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

    _chunk_size = 6

    def __init__(self, query_name, username, chat_id, increment):
        self._query_name    = query_name
        self._username       = username
        self._chat_id        = chat_id
        self._increment      = increment

        self._state          = None

    @staticmethod
    def get_max_size_name_of_all_options(all_options):
        return len(max((map(lambda x: ''.join(x[1:]), all_options))))

    def get_option_name_with_indent(self, all_options, name_data):
        max_str_size = self.get_max_size_name_of_all_options(all_options)
        str_size = len(''.join(name_data))
        whs_num = 1 if max_str_size - str_size == 0 else max_str_size - str_size
        whs = ' ' * int(whs_num * 2.3777 + 35)
        option_name = whs.join(name_data)
        return option_name

    def get_girls_options(self):
        user = session.query(User).filter_by(username=self._username).one()
        filters = {'Базовый': user.girls_filter, 'Расширенный': user.extended_girls_filter, 'Услуги': user.services}
        filter_ = filters.get(self._query_name)
        return filter_.as_list(filter_)

    def get_chunck_girls_options(self):
        girls_options = self.get_girls_options()
        return utils.chunk_list(girls_options, self._chunk_size)

    def get_part_from_chunk_girls_options(self):
        chunk_girls_options = self.get_chunck_girls_options()
        state = filters_state.get(self._chat_id, 0) + self._increment
        if state == len(chunk_girls_options):
            state = 0

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
        if self._state == 0:
            move_options = (self.move_options_data[1], )
        else:
            move_options = self.move_options_data

        move_options = (self.Option(name, callback.format(self._query_name)) for name, callback in move_options)
        return itertools.chain(options_objects, move_options)

    def get_keyboard_options(self):
        return self.add_move_options()


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
    def common_handler(common_name, filter_name, username, chat_id, message_id, increment=0):
        args = (filter_name, username, chat_id, increment)
        if common_name == 'filters':
            kb_options = FiltersCBQ(*args).get_keyboard_options()
        elif common_name == 'catalog':
            kb_options = CatalogCBQ(*args).get_keyboard_options()

        keyboard = utils.create_inline_keyboard_ext(*kb_options, prefix=f'{common_name}_option_', row_width=1)
        bot.edit_message_text(f'🅰️ *{filter_name}*', chat_id, message_id, parse_mode='Markdown', reply_markup=keyboard)
