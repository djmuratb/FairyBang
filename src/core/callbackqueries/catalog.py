# -*- coding: utf-8 -*-
from src.core.callbackqueries.base import BaseCBQ


class CatalogCBQ(BaseCBQ):
    __slots__ = ('_query_name', '_username', '_chat_id', '_increment')

    def __init__(self, query_name, username, chat_id, increment):
        self._query_name = query_name
        self._username = username
        self._chat_id = chat_id
        self._increment = increment

    def get_keyboard_options(self):
        return []
