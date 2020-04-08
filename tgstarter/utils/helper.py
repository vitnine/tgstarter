from typing import Any, List, Callable
from enum import Enum


def function_fullname(function: Callable[..., Any]) -> str:
    return f'{function.__module__}.{function.__name__}'


class Item:
    def __init__(self, value: Any = None) -> None:
        self._value = value

    def __get__(self, instance, owner) -> str:
        return self._value or ''

    def __set_name__(self, owner, name: str) -> None:
        if self._value is None:
            self._value = name


class NamedEnum(Enum):

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: List[Any]) -> str:
        return name
