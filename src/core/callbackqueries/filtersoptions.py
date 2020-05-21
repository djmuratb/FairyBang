# -*- coding: utf-8 -*-
import itertools
import collections as cs

from sqlalchemy import inspect, Column, ARRAY, Enum

from src.messages import *
from src.models import session, FILTERS, Services

from src.core.common import bot
from src.core.stepsprocesses import process_change_range_option_val_step, process_change_location_step
from src.core.utils.botutils import BotUtils, Keyboards
from src.core.callbackqueries.common import common_handler


class BaseMixin:
    _msg0 = 'Введите диапазон значений.'
    _msg1 = 'Введите значение от *{}* до *{}*.'
    _msg2 = 'Выберите один из вариантов.'
    _msg3 = 'Введите следующее значение: *{}*.'

    Option = cs.namedtuple('Option', ['name', 'callback'])

    def __init__(self, **kwargs):
        self._filter_name       = kwargs['filter_name']
        self._option_name_key   = kwargs['option_name_key']
        self._username          = kwargs['username']
        self._chat_id           = kwargs['chat_id']
        self._message_id        = kwargs['message_id']

        self._filter_class      = FILTERS.get(kwargs.get('filter_name'))

    def _add_move_back_option(self, options):
        move_cb = f'ch:back:{self._filter_name}'
        return itertools.chain(options, (self.Option(name='⬅️ Назад', callback=move_cb),))

    def _get_options(self, default_values, option_key, prefix):
        options = (
            self.Option(name=val, callback=f'{prefix}:{self._filter_name}:{option_key}:{val}')
            for val in default_values
        )
        return self._add_move_back_option(options)

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
            data = ('', 'other')

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

        return MSG_CHANGE_OPTION_VAL.format(text), value, value_type, column.key

    def get_selected_column(self):
        columns = inspect(self._filter_class).columns
        for col in columns:
            if col.key == self._option_name_key:
                return col

    def get_msg_data(self):
        selected_column = self.get_selected_column()
        return self.get_msg_data_from_column(selected_column)


class RangeMixin(BaseMixin):
    def send_range_msg(self, option_key, default_values, msg):
        chat_msg = bot.send_message(self._chat_id, msg, parse_mode='Markdown', reply_markup=KB_CANCEL)
        bot.register_next_step_handler(
            chat_msg,
            process_change_range_option_val_step,
            default_values=default_values,
            filter_class=self._filter_class,
            key=option_key,
        )


class EnumMixin(BaseMixin):

    def send_enum_msg(self, option_key, default_values, msg):
        options = self._get_options(default_values, option_key, prefix='ch')
        kb = Keyboards.create_inline_keyboard_ext(*options, row_width=2)
        bot.edit_message_text(msg, self._chat_id, self._message_id, parse_mode='Markdown', reply_markup=kb)


class ServicesMixin(BaseMixin):
    def _get_new_option_val(self):
        o = session.query(Services).filter_by(user_username=self._username).one()
        column = self.get_selected_column()
        current_option_val = o.__getattribute__(column.key)
        return (o, column.key, False) if current_option_val else (o, column.key, True)

    def send_service_msg(self):
        o, key, new_option_val = self._get_new_option_val()
        BotUtils.write_changes(o, key, new_option_val)
        common_handler('filters', self._filter_name, self._username, self._chat_id, self._message_id)


class LocationMixin(BaseMixin):

    def _send_other_location_msg(self, option_key, msg_text):
        msg = bot.send_message(self._chat_id, msg_text, self._message_id, parse_mode='Markdown', reply_markup=KB_CANCEL)
        bot.register_next_step_handler(
            msg,
            process_change_location_step,
            location=option_key,
        )

    def _send_country_msg(self, option_key, msg):
        options = self._get_options(AVAILABLE_COUNTRIES_LIST, option_key, prefix='filters:country')
        kb = Keyboards.create_inline_keyboard_ext(*options, row_width=1)
        bot.edit_message_text(msg, self._chat_id, self._message_id, parse_mode='Markdown', reply_markup=kb)

    def send_location_msg(self, option_key):
        msg = MSGS_LOCATIONS.get(option_key)
        if option_key == 'country':
            self._send_country_msg(option_key, msg)
            return

        self._send_other_location_msg(option_key, msg)


class OtherMixin(BaseMixin):
    def send_other_msg(self, option_key, default_values, msg):
        pass


class FiltersOptionsHandler(RangeMixin, EnumMixin, ServicesMixin, LocationMixin, OtherMixin):
    __slots__ = ('_send_msg_funcs',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._send_msg_funcs = {
            'range'  : self.send_range_msg,
            'enum'   : self.send_enum_msg,
            'other'  : self.send_other_msg_handler,
        }

    @staticmethod
    def is_location(option_key):
        if option_key in ('country', 'city', 'subway'):
            return True

    def send_other_msg_handler(self, option_key, default_values, msg):
        if self.is_location(option_key):
            self.send_location_msg(option_key)
            return

        self.send_other_msg(option_key, default_values, msg)

    def send_change_option_value_msg(self):
        if self._filter_class == Services:
            self.send_service_msg()
            return

        msg, default_values, value_type, key = self.get_msg_data()
        self._send_msg_funcs[value_type](key, default_values, msg)
