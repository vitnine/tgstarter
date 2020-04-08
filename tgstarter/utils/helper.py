from typing import Any, Callable


def function_fullname(function: Callable[..., Any]) -> str:
    return f'{function.__module__}.{function.__name__}'
