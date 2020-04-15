import types
from typing import Tuple, Type, Union


ExcInfo = Union[
    Tuple[None, None, None],
    Tuple[
        Type[BaseException],
        BaseException,
        types.TracebackType
    ]
]
