# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class ValidatorBase(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def validate(**kwargs):
        pass


class RangeValidator(ValidatorBase):
    @staticmethod
    def validate(**kwargs):
        value, default_values = kwargs.values()

        try:
            values = map(int, value.split('-'))
            start, end = values
        except ValueError:
            return

        for num in values:
            if num not in range(*default_values):
                return

        if start > end:
            return

        return start, end


class EnumValidator(ValidatorBase):
    @staticmethod
    def validate(**kwargs):
        value, enums = kwargs.values()
        value = value.capitalize()
        return value if value in enums else None


class LocationValidator(ValidatorBase):
    @staticmethod
    def validate(**kwargs):
        pass


VALIDATORS = {
    'range'     : RangeValidator,
    'enum'      : EnumValidator,
    'location'  : LocationValidator,
}
