from datetime import datetime
from enum import auto, Enum
from typing import Optional, Dict, Any

from pydantic import BaseModel
from aiogram import types

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


class Log(BaseModel):
    class Config:
        use_enum_values = True

    datetime: datetime
    level: LogLevel
    type: LogType

    came_from: EventFrom
    user_info: Optional[LogUserInfo]
    # user_id: int
    # chat_id: int
    # state: Optional[str]
    update: Dict[str, Any]

    exception: Optional[ExceptionModel]
