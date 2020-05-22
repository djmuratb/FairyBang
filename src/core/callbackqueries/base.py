# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class BaseCBQ(metaclass=ABCMeta):
    move_options_data = (('⬅️ Предыдущая', 'move_previous'), ('➡️️ Следующая', 'move_next'))

    @abstractmethod
    def get_keyboard_options(self):
        pass
