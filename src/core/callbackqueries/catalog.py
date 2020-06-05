# -*- coding: utf-8 -*-
from sqlalchemy.sql.sqltypes import INTEGER, VARCHAR, BOOLEAN
from sqlalchemy.dialects.postgresql.base import ENUM
from sqlalchemy.dialects.postgresql.array import ARRAY

from src.messages import *
from src.models import User, user_session, Girl, girl_session, UserGirlBaseFilter, UserGirlExtFilter, \
    UserGirlServices, GirlBaseFilter, GirlExtFilter

from src.core.helpers.types import KeyboardOption
from src.core.common import bot
from src.core.helpers.botutils import BotUtils


def create_main_catalog_keyboard(catalog_profiles_num):
    buttons = (
        (f'⚙️ ПОКАЗЫВАТЬ ПО   -   {catalog_profiles_num}', f'{PX_CAT_SET}profiles_num'),
        ('👠 ПОКАЗАТЬ АНКЕТЫ', f'{PX_CAT}{catalog_profiles_num}')
    )
    options = (KeyboardOption(name=name, callback=callback) for name, callback in buttons)
    return Keyboards.create_inline_keyboard_ext(*options, prefix='', row_width=1)


def set_catalog_profiles_limit(username, chat_id, message_id, new_val):
    def is_valid(val):
        return (val == 1 or val % 5 == 0) and val != 0

    if new_val:
        user = user_session.query(User).filter_by(username=username).one()
        BotUtils.write_changes(user, 'catalog_profiles_num', new_val)

        kb = create_main_catalog_keyboard(user.catalog_profiles_num)
        bot.edit_message_text(MSG_CATALOG, chat_id, message_id, parse_mode='Markdown', reply_markup=kb)
        bot.send_message(chat_id, MSG_SUCCESS_CHANGE_OPTION, parse_mode='Markdown')
    else:
        options = (KeyboardOption(name=f'{x}', callback=f'{PX_CAT_SET}profiles_num:{x}') for x in range(11) if is_valid(x))
        kb = Keyboards.create_inline_keyboard_ext(*options, prefix='', row_width=1)
        bot.edit_message_text(MSG_CATALOG_NUM_PROFILES, chat_id, message_id, parse_mode='Markdown', reply_markup=kb)


class CatalogBase:
    __slots__ = ('_username', '_chat_id', '_message_id')

    def __init__(self, **kwargs):
        self._username      = kwargs['username']
        self._chat_id       = kwargs['chat_id']
        self._message_id    = kwargs.get('message_id', None)


class CatPaymentDetail(CatalogBase):
    __slots__ = ('_girl_id', )

    def __init__(self, girl_id, **kwargs):
        super().__init__(**kwargs)
        self._girl_id = girl_id

    def send_payment_details(self):
        pass


class CatPayment(CatalogBase):
    __slots__ = ('_girl_id', )

    def __init__(self, girl_id, **kwargs):
        super().__init__(**kwargs)
        self._girl_id = girl_id

    def send_payment(self):
        pass


class CatProfileDetail(CatalogBase):
    __slots__ = ('_girl_id', )

    def __init__(self, girl_id, **kwargs):
        super().__init__(**kwargs)
        self._girl_id = girl_id

    def send_profile_detail(self):
        pass


class _GirlsSelectionMixin(CatalogBase):
    __slots__ = ('_profiles_limit', '_increment')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._profiles_limit    = kwargs.get('profiles_limit')
        self._increment         = kwargs.get('increment', 0)

    def get_user_filters(self):
        return user_session.\
            query(UserGirlBaseFilter, UserGirlExtFilter, UserGirlServices).\
            filter_by(user_username=self._username).one()


class CatProfiles(_GirlsSelectionMixin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def send_profiles(self):
        pass
