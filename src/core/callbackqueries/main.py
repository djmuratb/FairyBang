# -*- coding: utf-8 -*-
from src.messages import *
from src.core.common import bot
from src.core.stepsprocesses import process_promocode_step


class MainCBQ:
    @staticmethod
    def enter_promocode(chat_id):
        msg = bot.send_message(chat_id, MSG_ENTER_PROMO, parse_mode='Markdown', reply_markup=KB_CANCEL)
        bot.register_next_step_handler(msg, process_promocode_step)
