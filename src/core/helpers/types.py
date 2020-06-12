import collections as cs

from dataclasses import dataclass


KeyboardOption = cs.namedtuple('KeyboardOption', [
    'name',
    'callback',
])

ColumnResultSet = cs.namedtuple('ColumnResultSet', [
    'key',
    'name',
    'value',
    'type',
    'nullable',
])


@dataclass(repr=False, eq=False)
class FiltersState:
    base_filter: int    = 0
    ext_filter: int     = 0
    services: int       = 0
