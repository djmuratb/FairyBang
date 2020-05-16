# -*- coding: utf-8 -*-
from src.models import session, FILTERS

from src.core.common import bot

from src.core.callbackqueries.common import common_handler
from src.core.callbackqueries.filtersoptions import FiltersOptionsHandler

from src.core.stepsprocesses import process_city_step, process_promocode_step

from src.core.utils.botutils import BotUtils
from src.core.utils.validators import VALIDATORS

from src.messages import *


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

        common_handler('filters', filter_name, username, chat_id, message_id)

    @staticmethod
    def options_handler(common_name, filter_name, option_name, username, chat_id, message_id):
        args = (filter_name, option_name, username, chat_id, message_id)
        if common_name == 'filters':
            FiltersOptionsHandler(*args).send_change_option_value_msg()
        elif common_name == 'catalog':
            pass
