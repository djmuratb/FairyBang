# -*- coding: utf-8 -*-
import itertools

from src.models import user_session, FILTERS

from src.core.common import bot
from src.core.helpers.types import KeyboardOption
from src.core.helpers import pyutils
from src.core.helpers.botutils import Keyboards

from src.core.callbackqueries.extra import *
from src.core.callbackqueries.base import BaseCBQ


filters_state = {}


class FiltersCBQ(BaseCBQ):
    __slots__ = ('_filter_name', '_username', '_chat_id', '_increment')

    _chunk_size = 7

    def __init__(self, filter_name, username, chat_id, message_id, increment=0):
        self._filter_name    = filter_name
        self._username       = username
        self._chat_id        = chat_id
        self._message_id     = message_id
        self._increment      = increment

        self._state          = None
        self._add_move       = True
        self._move_options_data = (
            ('⬅️ Предыдущая', f'{PX_FIL_MOVE}{self._filter_name}:prev'),
            ('➡️️ Следующая', f'{PX_FIL_MOVE}{self._filter_name}:next')
        )

    @staticmethod
    def get_max_size_name_of_all_options(all_options):
        return len(
            max(
                (map(lambda x: ''.join(x[1:]), all_options))
            )
        )

    @staticmethod
    def get_option_as_str(data):
        option_key, option_value = data
        return f'{option_key}  -  ( {option_value} )'

    @property
    def girls_options(self):
        filter_ = FILTERS.get(self._filter_name)
        return filter_.as_tuple(
            user_session.query(filter_).filter(filter_.user_username == self._username).one()
        )

    def get_chunk_girls_options(self):
        return pyutils.chunk_list(self.girls_options, self._chunk_size)

    @property
    def part_from_chunk_girls_options(self):
        chunk_girls_options = self.get_chunk_girls_options()
        state = filters_state.get(self._chat_id, 0) + self._increment
        if state == len(chunk_girls_options):
            state = 0

        if len(chunk_girls_options) == 1:
            self._add_move = False

        filters_state[self._chat_id] = self._state = state
        return chunk_girls_options[state]

    def get_options_objects(self):
        prefix = f'{PX_FIL_OP}{self._filter_name}:'
        return (
            KeyboardOption(name=self.get_option_as_str(data), callback=prefix + key)
            for key, *data, _ in self.part_from_chunk_girls_options
        )

    @property
    def keyboard_options(self):
        options_objects = self.get_options_objects()

        if not self._add_move:
            return options_objects

        if self._state == 0:
            move_options = (self._move_options_data[1], )
        else:
            move_options = self._move_options_data

        move_options = (KeyboardOption(name, callback) for name, callback in move_options)
        return itertools.chain(options_objects, move_options)

    def send_message(self):
        keyboard = Keyboards.create_inline_keyboard_ext(*self.keyboard_options, prefix='', row_width=1)
        bot.edit_message_text(
            f'🅰️ *{self._filter_name}*',
            self._chat_id,
            self._message_id,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
