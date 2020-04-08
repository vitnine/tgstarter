from typing import (
    Any,
    Optional,
    Dict,
    Tuple,
    Callable,
)
import functools

from aiogram.dispatcher.storage import BaseStorage
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


def check_address(*args: Any, **kwargs: Any) -> Any:
    addresses = BaseStorage.check_address(*args, **kwargs)
    return tuple(map(str, addresses))


def resolve_address(function: Callable[..., Any]) -> Callable[..., Any]:

    @functools.wraps(function)
    async def wrapper(self, *, chat: Optional[str], user: Optional[str], **kwargs) -> Tuple[int, int]:
        chat, user = check_address(chat=chat, user=user)
        return await function(self, chat=chat, user=user, **kwargs)

    return wrapper


def filter_chat_user(chat: Optional[str], user: Optional[str]) -> Dict[str, Optional[str]]:
    return dict(chat_id=chat, user_id=user)


class MongoStorage(BaseStorage):
    def __init__(self, mongo_client: AsyncIOMotorClient, mongo_database: AsyncIOMotorDatabase) -> None:
        self.client = mongo_client
        self.db = mongo_database

    async def close(self) -> None:
        pass

    async def wait_closed(self) -> None:
        pass

    def has_bucket(self) -> bool:
        return True

    @resolve_address
    async def get_state(
        self,
        *,
        chat: Optional[str] = None,
        user: Optional[str] = None,
        default: Optional[str] = None
    ) -> Optional[str]:

        result = await self.db.users.find_one(
            filter=filter_chat_user(
                chat=chat,
                user=user
            ),
            projection={
                '_id': False,
                'state': True
            }
        )
        return result['state'] if result else default

    @resolve_address
    async def set_state(
        self,
        *,
        chat: Optional[str] = None,
        user: Optional[str] = None,
        state: Optional[str] = None
    ) -> None:

        await self.db.users.update_one(
            filter=filter_chat_user(
                chat=chat,
                user=user
            ),
            update={
                '$set': {'state': state}
            },
            upsert=True
        )

    @resolve_address
    async def get_data(
        self,
        *,
        chat: Optional[str] = None,
        user: Optional[str] = None,
        default: Optional[Dict] = None
    ) -> Optional[Dict[Any, Any]]:

        result = await self.db.users.find_one(
            filter=filter_chat_user(
                chat=chat,
                user=user
            ),
            projection={
                '_id': False,
                'state_data': True
            }
        )
        return result['state_data'] if result else default

    @resolve_address
    async def set_data(
        self,
        *,
        data: Optional[Dict],
        chat: Optional[str] = None,
        user: Optional[str] = None
    ) -> None:

        await self.db.users.update_one(
            filter=filter_chat_user(
                chat=chat,
                user=user
            ),
            update={
                '$set': {'state_data': data}
            },
            upsert=True
        )

    update_data = set_data

    @resolve_address
    async def reset_data(self, *, chat: Optional[str] = None, user: Optional[str] = None) -> None:
        await self.db.users.update_one(
            filter=filter_chat_user(
                chat=chat,
                user=user
            ),
            update={
                '$set': {
                    'state_data': {}
                }
            }
        )

    # # #

    @resolve_address
    async def reset_state(self, *, chat: Optional[str] = None, user: Optional[str] = None) -> None:
        raise NotImplementedError

    @resolve_address
    async def finish(self, *, chat: Optional[str] = None, user: Optional[str] = None) -> None:
        raise NotImplementedError

    @resolve_address
    async def get_bucket(
        self,
        *,
        chat: Optional[str] = None,
        user: Optional[str] = None,
        default: Optional[Dict] = None
    ) -> Optional[Dict]:

        result = await self.db.users.find_one(
            filter=filter_chat_user(
                user=user,
                chat=chat
            ),
            projection={
                '_id': False,
                'bucket': True
            }
        )
        return result['bucket'] if result else default

    @resolve_address
    async def set_bucket(
        self,
        *,
        chat: Optional[str] = None,
        user: Optional[str] = None,
        bucket: Optional[Dict] = None
    ) -> None:

        await self.db.users.update_one(
            filter=filter_chat_user(
                chat=chat,
                user=user
            ),
            update={
                '$set': {
                    'bucket': bucket if bucket is not None else {}
                }
            },
            upsert=True
        )

    @resolve_address
    async def update_bucket(
        self,
        *,
        chat: Optional[str] = None,
        user: Optional[str] = None,
        bucket: Optional[Dict] = None,
        **kwargs
    ) -> None:

        kwargs.update({} if bucket is None else bucket)
        await self.db.users.update_one(
            filter=filter_chat_user(
                chat=chat,
                user=user
            ),
            update={
                '$set': {'bucket': kwargs}
            },
            upsert=True
        )

    @resolve_address
    async def reset_bucket(self, *, chat: Optional[str] = None, user: Optional[str] = None) -> None:
        await self.db.users.update_one(
            filter=filter_chat_user(
                chat=chat,
                user=user
            ),
            update={
                '$set': {
                    'bucket': {}
                }
            }
        )
