# -*- coding: utf-8 -*-
import collections as cs

from abc import ABCMeta, abstractmethod


class BaseCBQ(metaclass=ABCMeta):
    Option = cs.namedtuple('Option', ['name', 'callback'])
    move_options_data = (('⬅️ Предыдущая', 'move_previous'), ('➡️️ Следующая', 'move_next'))

    @abstractmethod
    def get_keyboard_options(self):
        pass
