# -*- coding: utf-8 -*-
import os
import yaml


def get_abs_path(file):
    return os.path.join(
        os.getcwd(), file
    )


def load_config(cfg):
    path = get_abs_path(cfg)

    with open(path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)
