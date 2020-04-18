from typing import (
    Optional,
    Union,
    List,
    Tuple,
)

from tgstarter.utils import helper


def fullname_jinja2_filter(names: Union[List[str], Tuple[str, Optional[str]]]) -> str:
    first_name, last_name = names
    return helper.user_fullname(first_name=first_name, last_name=last_name)
