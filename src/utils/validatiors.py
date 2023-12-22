from typing import Iterable


def ignore_none_values(object: Iterable) -> dict:
    return {key: value for key, value in object if value is not None}


def ignore_none_values_and_empty_list(object: Iterable) -> dict:
    return {key: value for key, value in object if value is not None and value != []}
