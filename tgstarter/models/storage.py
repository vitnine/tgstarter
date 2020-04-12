from datetime import datetime
from enum import auto
from typing import Optional, Dict, Any

from pydantic import BaseModel

from tgstarter.utils.helper import NamedEnum


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


class UserInfo(BaseModel):
    user_id: int
    chat_id: int


class Log(BaseModel):
    class Config:
        use_enum_values = True

    datetime: datetime
    level: LogLevel
    type: LogType

    came_from: EventFrom
    user_info: Optional[UserInfo]
    # user_id: int
    # chat_id: int
    # state: Optional[str]
    data: Dict[str, Any]

    exception: Optional[ExceptionModel]
