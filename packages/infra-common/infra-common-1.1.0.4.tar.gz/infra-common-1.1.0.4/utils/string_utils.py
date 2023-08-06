import random

import re
import typing
from random import shuffle
from typing import Optional


def is_none_or_empty(s: Optional[str]) -> bool:
    return not s


def is_empty(s: str) -> bool:
    if s is None:
        raise ValueError('String is None')
    return len(s) == 0


def is_not_empty(s: Optional[str]) -> bool:
    return not is_none_or_empty(s)


def from_hex(value: str) -> int:
    return int(value, 16)


def version_to_tuple(version_str: str, ignore_non_digits_or_dots: bool = False) -> typing.List[int]:
    if not isinstance(version_str, str):
        raise TypeError(f'version_str should be a string and not {type(version_str)}')
    if is_empty(version_str):
        return []
    if ignore_non_digits_or_dots:
        version_str = re.sub(r'([^\d.]+)', '', version_str)
    if not re.match('^[0-9][0-9.]*$', version_str):
        raise ValueError(f'version string must be dot separated numbers only. Instead got {version_str}')
    return [int(x) for x in version_str.split('.')]


def remove_non_digit_characters(s: str):
    if s is None:
        return None
    return re.sub(r'([^\d]+)', '', s)


def find_all(substring, full_string):
    return [m.start() for m in re.finditer(substring, full_string)]


def shuffle_flags_for_commands(command):
    parts = command.split('/')
    new_command = parts.pop(0)
    shuffle(parts)
    for item in parts:
        new_command += f' /{item}'
    return new_command


def random_choice_string(lst: [str]):
    if lst is None or len(lst) is 0:
        return ''
    return random.choice(lst)
