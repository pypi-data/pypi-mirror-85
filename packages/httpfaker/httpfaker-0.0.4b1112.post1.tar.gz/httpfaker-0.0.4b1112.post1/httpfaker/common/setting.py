import os

import yaml
import json

from httpfaker.common.logger import log
from httpfaker.common.tools import check_path

__all__ = ['get_yaml', 'check_valid', 'update_settings']


def check_valid(key, value):
    if not value:
        log.e('[%s] Not Configured.Please Config in settings.yaml.' % key)
        raise ValueError
    return value


def get_yaml(file_path=None):
    yaml_file = check_path(file_path)
    with open(yaml_file, 'r', encoding='utf-8') as f:
        if yaml_file.endswith('.yml') or yaml_file.endswith('.yaml'):
            return yaml.safe_load(f.read())
        elif yaml_file.endswith('.json'):
            return json.loads(f.read())


def update_settings(setting_data):
    register_setting = setting_data.get("Register")
    _global_setting = setting_data.get("global")
    for register_module in register_setting:
        for g in _global_setting:
            if g not in register_setting[register_module]:
                register_setting[register_module][g] = _global_setting[g]

    return setting_data
