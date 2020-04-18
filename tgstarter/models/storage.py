from datetime import datetime
from typing import Optional, Dict, Any, List

from pydantic import BaseModel

from tgstarter.utils.helper import NamedEnum, auto


class EventFrom(str, NamedEnum):
    USER = auto()
    BOT = auto()


class LogType(str, NamedEnum):
    EVENT = auto()
    # NOTIFICATION = auto()
    TASK = auto()


class LogLevel(str, NamedEnum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class ExceptionModel(BaseModel):
    type: str
    value: str
    traceback: str


class LogUserInfo(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # chat: types.Chat
    # user: types.User
    chat: Dict[str, Any]
    user: Dict[str, Any]


class LogTask(BaseModel):
    function_fullname: str
    args: List[Any]
    kwargs: Dict[str, Any]
    result: Optional[str]


class Log(BaseModel):
    class Config:
        use_enum_values = True

    datetime: datetime
    level: LogLevel
    type: LogType

    came_from: EventFrom
    user_info: Optional[LogUserInfo]
    # state: Optional[str]
    update: Optional[Dict[str, Any]]
    task: Optional[Dict[str, Any]]

    exception: Optional[ExceptionModel]
