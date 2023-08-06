import re
import typing
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
