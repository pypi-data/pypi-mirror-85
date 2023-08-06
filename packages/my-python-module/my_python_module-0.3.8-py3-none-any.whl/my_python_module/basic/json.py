#!/usr/bin/env python
# -*-coding:utf-8-*-


import os
import json


def write_json(file, data):
    """
    write data to json file
    """
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_json_file(json_filename, default_data=None):
    """
    try get json file or auto-create the json file with default_data
    """
    default_data = default_data if default_data is not None else {}

    if not os.path.exists(json_filename):
        data = default_data
        write_json(json_filename, data)

    return json_filename


def get_json_data(json_filename, default_data=None):
    """
    get json file data
    """
    with open(get_json_file(json_filename, default_data=default_data),
              encoding='utf8') as f:
        data = json.load(f)
        return data


def get_json_value(json_filename, key, default_data=None):
    """
    get value by key in json file if your json file stored value as one dict.
    """
    data = get_json_data(json_filename, default_data=default_data)
    if not isinstance(data, dict):
        raise Exception(
            "the target json file must stored whole data as one dict.")

    return data.get(key)


def set_json_value(json_filename, key, value, default_data=None):
    """
    set value by key and value in json file if your json file stored value
    as one dict.
    """
    data = get_json_data(json_filename, default_data=default_data)

    if not isinstance(data, dict):
        raise Exception(
            "the target json file must stored whole data as one dict.")

    data[key] = value
    write_json(get_json_file(json_filename), data)
