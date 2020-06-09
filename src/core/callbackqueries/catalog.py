# -*- coding: utf-8 -*-
import itertools
import functools

from sqlalchemy import or_, func
from sqlalchemy.orm import subqueryload
from sqlalchemy.sql.sqltypes import VARCHAR
from sqlalchemy.dialects.postgresql.base import ENUM
from sqlalchemy.dialects.postgresql.array import ARRAY

from src.messages import *
from src.models import User, user_session, Girl, girl_session, UserGirlBaseFilter, UserGirlExtFilter, \
    UserGirlServices, GirlBaseFilter, GirlExtFilter, GirlServices

from src.core.common import bot
from src.core.helpers import pyutils
from src.core.helpers.types import KeyboardOption
from src.core.helpers.botutils import BotUtils


OFFSET_STATE = {}


@functools.lru_cache(None)
def get_total_profiles():
    return girl_session.query(func.count(Girl.id)).scalar()


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

        msg = MSG_CATALOG.format(get_total_profiles())
        kb = create_main_catalog_keyboard(user.catalog_profiles_num)
        bot.edit_message_text(msg, chat_id, message_id, parse_mode='Markdown', reply_markup=kb)
        bot.send_message(chat_id, MSG_SUCCESS_CHANGE_OPTION, parse_mode='Markdown')
    else:
        bot.edit_message_text(
            MSG_CATALOG_NUM_PROFILES,
            chat_id,
            message_id,
            parse_mode='Markdown',
            reply_markup=Keyboards.create_inline_keyboard_ext(
                *(
                    KeyboardOption(name=f'{x}', callback=f'{PX_CAT_SET}profiles_num:{x}')
                    for x in range(11)
                    if is_valid(x)
                ), prefix='', row_width=1
            )
        )


class CatalogBase:
    __slots__ = ('_username', '_chat_id', '_message_id', '_profiles_limit')

    _more_girls_text = '🔵 Показать еще 🔵'

    def __init__(self, **kwargs):
        self._username          = kwargs['username']
        self._chat_id           = kwargs['chat_id']
        self._message_id        = kwargs.get('message_id', None)
        self._profiles_limit    = kwargs.get('profiles_limit')

    def _get_kb_with_more_btn(self, *buttons):
        more_girls_btn = KeyboardOption(name=self._more_girls_text, callback=f'{PX_CAT_MORE}{self._profiles_limit}')
        return Keyboards.create_inline_keyboard_ext(*buttons, more_girls_btn, row_width=1)


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

    _default_item_emoji     = '📁'
    _exist_service_emoji    = '☑️'
    _pay_btn_name           = '💳 Заказать'
    _include_col_names      = (
        #   --- GIRL ---

        #   --- BASE FILTER ---
        'Возраст', 'Рост', 'Грудь',
        #   --- EXT FILTER ---
        'Национальность', 'Цвет волос', 'Апартаменты 1 час', 'Выезд к Вам', 'Выезд к Вам на ночь'
    )

    def __init__(self, girl_id, **kwargs):
        super().__init__(**kwargs)
        self._girl_id = girl_id

    @property
    def _keyboard(self):
        btn = KeyboardOption(name=self._pay_btn_name, callback=f'{PX_CAT_PAY}{self._profiles_limit}:{self._girl_id}')
        return self._get_kb_with_more_btn(btn)

    def _get_personal_info(self, girl):
        return itertools.chain(
            girl.as_tuple(girl, include_col_names=self._include_col_names, meta='girl'),
            girl.base_filter.as_tuple(girl.base_filter, include_col_names=self._include_col_names, meta='girl'),
            girl.ext_filter.as_tuple(girl.ext_filter, include_col_names=self._include_col_names, meta='girl')
        )

    @staticmethod
    def _add_about(msg, about_text):
        if about_text:
            msg += f'{about_text}\n'

        return msg

    def _get_personal_info_msg(self, girl):
        msg_detail_info = MSG_GIRL_DETAIL_INFO.format(name=girl.name)
        msg_detail_info = self._add_about(msg_detail_info, girl.about)

        msg_personal_info = MSG_GIRL_PERSONAL_INFO

        for el in self._get_personal_info(girl):
            msg_personal_info += f'{self._default_item_emoji} {el.name}: *{el.value}*\n'

        return msg_detail_info + msg_personal_info

    def _get_services_msg(self, girl):
        services_msg = MSG_GIRL_DETAIL_SERVICES
        for el in girl.services.as_tuple(girl.services, meta='girl'):
            if el.value == 'да':
                services_msg += f'{self._exist_service_emoji} *{el.name}*\n'

        return services_msg

    def send_profile_detail(self):
        girl = girl_session.query(Girl).get(self._girl_id)
        msg = self._get_personal_info_msg(girl) + self._get_services_msg(girl)
        bot.edit_message_text(msg, self._chat_id, self._message_id, reply_markup=self._keyboard, parse_mode='Markdown')


class _GirlsSelectionMixin(CatalogBase):
    __slots__ = ('_profiles_limit', '_more_profiles', '_order_by')

    _default_enum_value = 'Не важно'
    _exclude_columns_names = ('country', )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._order_by          = kwargs.get('order_by', GirlBaseFilter.price)
        self._more_profiles     = kwargs.get('more', False)

    @property
    def _slice_range(self):
        if self._more_profiles:
            offset = OFFSET_STATE.get(self._chat_id, 0)
            end = offset + self._profiles_limit
        else:
            offset = 0
            end = offset + self._profiles_limit

        OFFSET_STATE[self._chat_id] = end
        return offset, end

    @staticmethod
    def _get_services_items(user_services_instance):
        return dict(filter(
            lambda elem: elem[1] is True, user_services_instance.items()
        ))

    def _get_sql_condition(self, table, key, val, type_, nullable):
        t_key = table.c[key]

        if type_ == VARCHAR:
            return t_key == val

        if type_ == ENUM and val.value != self._default_enum_value:
            return t_key == val.value

        if type_ == ARRAY and val:
            if nullable:
                return or_(t_key.is_(None), t_key.in_(range(*val)))
            else:
                return t_key.in_(range(*val))

    def _get_filter_items(self, girl_filter_class, user_filter_instance):
        table = girl_filter_class.__table__
        ufi = user_filter_instance
        return filter(
            lambda x: x is not None,
            (
                self._get_sql_condition(table, key, val, type_, nullable)
                for key, _, val, type_, nullable in ufi.as_tuple(ufi, format_value=False)
                if key not in self._exclude_columns_names
            )
        )

    def _get_user_filters_instances(self):
        return user_session.\
            query(UserGirlBaseFilter, UserGirlExtFilter, UserGirlServices).\
            filter_by(user_username=self._username).one()

    @property
    def girls(self):
        # NOTE: попробовать в query подгружать только определенные поля у relationships
        user_base_filter, user_ext_filter, user_services = self._get_user_filters_instances()

        user_base_filter_items = self._get_filter_items(GirlBaseFilter, user_base_filter)
        user_ext_filter_items = self._get_filter_items(GirlExtFilter, user_ext_filter)
        user_services_items = self._get_services_items(user_services.as_dict(user_services, only_key_val=True))

        return girl_session. \
            query(Girl). \
            join(Girl.base_filter).options(subqueryload(Girl.base_filter)). \
            filter(
                GirlBaseFilter.country == user_base_filter.country.split(' ')[-1],
                *user_base_filter_items
            ). \
            join(Girl.ext_filter).options(subqueryload(Girl.ext_filter)). \
            filter(*user_ext_filter_items). \
            join(Girl.services).options(subqueryload(Girl.services)). \
            filter_by(**user_services_items). \
            order_by(self._order_by). \
            slice(*self._slice_range). \
            values(Girl.id, Girl.name, GirlBaseFilter.age, GirlBaseFilter.price, Girl.preview_photo)


class CatProfiles(_GirlsSelectionMixin):
    _short_description  = '{} | {} | {}р.'
    _more_detail_text   = '❣️ ПОДРОБНЕЕ ❣️'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_keyboard(self, id_, last):
        callback = f'{PX_CAT_PROFILE}{self._profiles_limit}:{id_}'
        more_detail_btn = KeyboardOption(name=self._more_detail_text, callback=callback)
        if not last:
            return Keyboards.create_inline_keyboard_ext(more_detail_btn, row_width=1)

        return self._get_kb_with_more_btn(more_detail_btn)

    def _send_profile_msg(self, id_, info, last):
        msg = MSG_GIRL_SHORT_INFO.format(*info)
        bot.send_message(self._chat_id, msg, reply_markup=self._get_keyboard(id_, last), parse_mode='Markdown')

    def send_profiles(self):
        try:
            for id_, *info, preview_photo, last in pyutils.lookahead(self.girls):
                bot.send_photo(self._chat_id, preview_photo)
                self._send_profile_msg(id_, info, last)
        except RuntimeError:
            bot.send_message(self._chat_id, MSG_GIRLS_OVER_EXC, reply_markup=KB_MENU, parse_mode='Markdown')
