# -*- coding: utf-8 -*-
from src.messages import *
from src.models import User, user_session, Girl, girl_session, UserGirlBaseFilter, UserGirlExtFilter, \
    UserGirlServices, GirlBaseFilter, GirlExtFilter

from src.core.helpers.types import Option
from src.core.common import bot
from src.core.helpers.botutils import BotUtils
from src.core.callbackqueries.base import BaseCBQ


def create_main_catalog_keyboard(catalog_profiles_num):
    buttons = (
        (f'⚙️ ПОКАЗЫВАТЬ ПО   -   {catalog_profiles_num}', f'{PX_CAT_SET}profiles_num'),
        ('👠 ПОКАЗАТЬ АНКЕТЫ', f'{PX_CAT}{catalog_profiles_num}')
    )
    options = (Option(name=name, callback=callback) for name, callback in buttons)
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
        options = (Option(name=f'{x}', callback=f'{PX_CAT_SET}profiles_num:{x}') for x in range(11) if is_valid(x))
        kb = Keyboards.create_inline_keyboard_ext(*options, prefix='', row_width=1)
        bot.edit_message_text(MSG_CATALOG_NUM_PROFILES, chat_id, message_id, parse_mode='Markdown', reply_markup=kb)


class GirlFilterMixin:
    pass


class CatalogCBQ(BaseCBQ):
    __slots__ = ('_query_name', '_username', '_chat_id', '_increment')

    def __init__(self, profiles_limit, username, chat_id, increment=0):
        self._profiles_limit = profiles_limit
        self._username = username
        self._chat_id = chat_id
        self._increment = increment

    def get_user_filters(self):
        return user_session.\
            query(UserGirlBaseFilter, UserGirlExtFilter, UserGirlServices).\
            filter_by(user_username=self._username).one()

    def foo(self, instance):
        lst = []
        pattern_range = re.compile(r'не задано')
        pattern_enum = re.compile(r'')

    def send_message(self):
        """
        Useful:
        # func name - send_previews
        # query = girl_session.query(Girl).offset(2).limit(1).all()
        # вывести имя , фото и id для колбэка

        !!! сделать разные класс методы , чтобы не дергать каждый раз полностью все объекты девушек

        # FIXME:
        1.сделать отдельную функцию для сбора фильтра диапазонов

        # TODO:
        2. получить данные по фильтрам , который задал пользователь
        3. сделать выборку из бд с учетом лимита , сдвига и фильтров
        4. сделать инлайн клавы для каждой девушки
        5. вывести сообщения с превьюхами

        """
        user_base_filter, user_ext_filter, user_services = self.get_user_filters()

        from sqlalchemy import or_, tuple_, and_
        from sqlalchemy.orm import subqueryload

        print(user_base_filter.as_tuple(user_base_filter))
        print(user_ext_filter.as_tuple(user_ext_filter))
        print(user_services.as_tuple(user_services))
        # res = user_ext_filter.__class__
        # print(res)
        #
        # print(222, res.category.property.columns)
        # print(333, res.__dict__['category'].property.columns)


        # for el in user_ext_filter.as_tuple(user_ext_filter):
        #     print(el)

        # girls = girl_session.\
        #     query(Girl).\
        #     join(Girl.base_filter).options(subqueryload(Girl.base_filter)). \
        #     filter(
        #         GirlBaseFilter.country == user_base_filter.country.split(' ')[-1],
        #         GirlBaseFilter.city == user_base_filter.city,
        #         # GirlBaseFilter.subway == user_base_filter.subway
        #
        #         GirlBaseFilter.age.in_(range(*user_base_filter.age)),
        #         or_(GirlBaseFilter.height.is_(None), GirlBaseFilter.height.in_(range(*user_base_filter.height))),
        #         or_(GirlBaseFilter.chest.is_(None), GirlBaseFilter.chest.in_(range(*user_base_filter.chest))),
        #
        #         GirlBaseFilter.price.in_(range(*user_base_filter.price)),
        #     ). \
        #     join(Girl.ext_filter).options(subqueryload(Girl.ext_filter)). \
        #     filter(
        #         # or_(GirlExtFilter.category == 'Не важно', GirlExtFilter.category == user_ext_filter.category.value),
        #         # or_(GirlExtFilter.hair_color == 'Не важно', GirlExtFilter.hair_color == user_ext_filter.hair_color.value),
        #         # or_(GirlExtFilter.body_type == 'Не важно', GirlExtFilter.body_type == user_ext_filter.body_type.value),
        #         # or_(GirlExtFilter.category == 'Не важно', GirlExtFilter.category == user_ext_filter.category.value),
        #         # or_(GirlExtFilter.category == 'Не важно', GirlExtFilter.category == user_ext_filter.category.value),
        #         # or_(GirlExtFilter.category == 'Не важно', GirlExtFilter.category == user_ext_filter.category.value),
        #         # or_(GirlExtFilter.category == 'Не важно', GirlExtFilter.category == user_ext_filter.category.value),
        #     ).all()

        # girls = girl_session.\
        #     query(Girl).\
        #     join(Girl.base_filter).options(subqueryload(Girl.base_filter)). \
        #     filter(
        #         GirlBaseFilter.age.in_(range(*user_base_filter.age))
        #     ). \
        #     join(Girl.ext_filter).options(subqueryload(Girl.ext_filter)). \
        #     filter(
        #         # or_(GirlExtFilter.category == 'Не важно', GirlExtFilter.category == user_ext_filter.category.value),
        #     ).\
        #     join(Girl.services).options(subqueryload(Girl.services)).\
        #     filter_by(
        #         # anal=user_services.anal,
        #     ).all()

        # print(girls)
        #
        # for o in girls:
        #     print(o.__dict__)
