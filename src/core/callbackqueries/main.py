# -*- coding: utf-8 -*-
import collections as cs

from src.models import session, FILTERS

from src.core.common import bot

from src.core.callbackqueries.common import common_handler
from src.core.callbackqueries.filtersoptions import FiltersOptionsHandler

from src.core.stepsprocesses import process_promocode_step, process_change_location_step

from src.core.utils.botutils import BotUtils
from src.core.utils.validators import VALIDATORS

from src.models import User, GirlsFilter
from src.messages import *


class MainCBQ:

    @staticmethod
    def set_catalog_profiles_num(username, chat_id, message_id, new_val):
        Option = cs.namedtuple('Option', ['name', 'callback'])

        if new_val:
            user = session.query(User).filter_by(username=username).one()
            BotUtils.write_changes(user, 'catalog_profiles_num', new_val)

            buttons = (f'⚙️ ПОКАЗЫВАТЬ ПО   -   {user.catalog_profiles_num}', '👠 ПОКАЗАТЬ АНКЕТЫ')
            kb = Keyboards.create_inline_keyboard(*buttons, prefix=f'main_profiles_num', row_width=1)

            bot.edit_message_text(MSG_CATALOG, chat_id, message_id, parse_mode='Markdown',reply_markup=kb)
            bot.send_message(chat_id, MSG_SUCCESS_CHANGE_OPTION, parse_mode='Markdown')
        else:
            options = (Option(name=f'{x}', callback=f'main_profiles_num:{x}') for x in range(1, 6))
            kb = Keyboards.create_inline_keyboard_ext(*options, prefix='', row_width=1)

            bot.edit_message_text(MSG_CATALOG_NUMBER_PROFILES, chat_id, message_id, parse_mode='Markdown', reply_markup=kb)

    @staticmethod
    def enter_promocode(chat_id):
        msg = bot.send_message(chat_id, MSG_ENTER_PROMO, parse_mode='Markdown', reply_markup=KB_CANCEL)
        bot.register_next_step_handler(msg, process_promocode_step)

    @staticmethod
    def change_enum_option_value(filter_name, option_key, value, username, chat_id, message_id):
        filter_class = FILTERS.get(filter_name)
        is_valid = VALIDATORS.get('enum').validate(enum_key=option_key, value=value)

        if is_valid:
            obj = session.query(filter_class).filter_by(user_username=username).one()
            BotUtils.write_changes(obj, option_key, value)

        common_handler('filters', filter_name, username, chat_id, message_id)

    @staticmethod
    def change_country_option_value(country, username, chat_id):
        BotUtils.write_changes(GirlsFilter, 'country', country, filter_by={'user_username': username})

        msg = bot.send_message(chat_id, MSGS_LOCATIONS['city'], parse_mode='Markdown', reply_markup=KB_CANCEL)
        bot.register_next_step_handler(msg, process_change_location_step, location='city')

    @staticmethod
    def options_handler(common_name, filter_name, option_name_key, username, chat_id, message_id):
        if common_name == 'filters':
            FiltersOptionsHandler(**locals()).send_change_option_value_msg()
        elif common_name == 'catalog':
            pass
