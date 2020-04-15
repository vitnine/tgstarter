from datetime import datetime
from enum import auto, Enum
from typing import Optional, Dict, Any, List

from pydantic import BaseModel
# from aiogram import types

from tgstarter.utils.helper import NamedEnum


class EventFrom(str, NamedEnum):
    USER: Enum = auto()
    BOT: Enum = auto()


class LogType(str, NamedEnum):
    EVENT: Enum = auto()
    # NOTIFICATION: Enum = auto()
    TASK: Enum = auto()


class LogLevel(str, NamedEnum):
    DEBUG: Enum = auto()
    INFO: Enum = auto()
    WARNING: Enum = auto()
    ERROR: Enum = auto()
    CRITICAL: Enum = auto()


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
