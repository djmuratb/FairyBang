# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class BaseCBQ(metaclass=ABCMeta):
    @abstractmethod
    def send_message(self):
        pass
