# -*- coding: utf-8 -*-
import os
import re

import yaml

from datetime import datetime, date
from collections import ChainMap
from itertools import islice


def get_abs_path(file: str):
    return os.path.join(
        os.getcwd(), file
    )


def load_config(cfg: str):
    path = get_abs_path(cfg)
    with open(path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def merge_list_of_dicts(lst: list):
    return dict(ChainMap(*lst))


def get_delta_days_from_dates(first: datetime, latest: datetime = datetime.now()):
    return (latest - first).days


def chunk_dict(data: dict, parts_num: int):
    it = iter(data)
    return [
        {key: data[key] for key in islice(it, parts_num)} for i in range(0, len(data), parts_num)
    ]


def chunk_list(data: list, parts_num: int):
    it = iter(data)
    return [
        [d for d in islice(it, parts_num)] for i in range(0, len(data), parts_num)
    ]


def set_attrs_values_from_dict(d: dict, obj: object, date_specific=False):
    pattern = re.compile(r'\d{4}(-\d{1,2})+')

    for key, value in d.items():
        if date_specific:
            val = date(*map(int, value.split('-'))) if re.match(pattern, str(value)) else value
        else:
            val = value

        obj.__setattr__(key, val)
