# -*- coding: utf-8 -*-
from src.messages import *

from src.core.common import bot
from src.core.stepsprocesses import process_change_city_step

from src.core.utils.botutils import BotUtils, Keyboards


def process_change_country_step(country_name, username, chat_id):
    user = BotUtils.create_user(username)
    BotUtils.write_changes(user.girls_filter, 'country', country_name)

    msg = bot.send_message(chat_id, MSG_ENTER_CITY, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_change_city_step)

