import types
from typing import (
    TypeVar,
    Tuple,
    Type,
    Union,
    Callable,
    Awaitable,
)


FilledExcInfo = Tuple[
    Type[BaseException],
    BaseException,
    types.TracebackType
]
ExcInfo = Union[
    Tuple[None, None, None],
    FilledExcInfo
]

AsyncCallbackVar = TypeVar('AsyncCallback', bound=Callable[..., Awaitable])
Handler = Callable[..., Callable[[AsyncCallbackVar], AsyncCallbackVar]]
