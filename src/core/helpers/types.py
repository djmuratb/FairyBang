import collections as cs


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
