# -*- coding: utf-8 -*-
from src.messages import *
from src.core.common import bot
from src.core.stepsprocesses import process_promocode_step


class MainCBQ:

    # @staticmethod
    # def set_num_profiles_per_page(username, chat_id, message_id, new_val):
    #     # TODO: move to catalog module
    #     def is_valid(val):
    #         return (val == 1 or val % 5 == 0) and val != 0
    #
    #     if new_val:
    #         user = session.query(User).filter_by(username=username).one()
    #         BotUtils.write_changes(user, 'catalog_profiles_num', new_val)
    #
    #         kb = create_main_catalog_keyboard(user.catalog_profiles_num)
    #         bot.edit_message_text(MSG_CATALOG, chat_id, message_id, parse_mode='Markdown', reply_markup=kb)
    #         bot.send_message(chat_id, MSG_SUCCESS_CHANGE_OPTION, parse_mode='Markdown')
    #     else:
    #         options = (Option(name=f'{x}', callback=f'main_profiles_num:{x}') for x in range(11) if is_valid(x))
    #         kb = Keyboards.create_inline_keyboard_ext(*options, prefix='', row_width=1)
    #         bot.edit_message_text(MSG_CATALOG_NUM_PROFILES, chat_id, message_id, parse_mode='Markdown', reply_markup=kb)

    @staticmethod
    def enter_promocode(chat_id):
        msg = bot.send_message(chat_id, MSG_ENTER_PROMO, parse_mode='Markdown', reply_markup=KB_CANCEL)
        bot.register_next_step_handler(msg, process_promocode_step)
