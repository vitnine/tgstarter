from typing import (
    Union,
    List,
    Tuple,
)

from tgstarter.utils import helper


def fullname_jinja2_filter(names: Union[List[str], Tuple[str, str]]) -> str:
    return helper.user_fullname(*names)
