from typing import (
    Any,
    Optional,
    Dict,
    Tuple,
)
import functools

import addict
from aiogram.dispatcher.storage import BaseStorage
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from tgstarter.utils.typing import AsyncCallbackVar


def check_address(*args: Any, **kwargs: Any) -> Any:
    addresses = BaseStorage.check_address(*args, **kwargs)
    return tuple(map(int, addresses))


def resolve_address(function: AsyncCallbackVar) -> AsyncCallbackVar:

    @functools.wraps(function)
    async def wrapper(self, *, chat: Optional[int], user: Optional[int], **kwargs) -> Tuple[int, int]:
        chat, user = check_address(chat=chat, user=user)
        return await function(self, chat=chat, user=user, **kwargs)

    return wrapper


def filter_chat_user(chat: Optional[int], user: Optional[int]) -> Dict[str, Optional[int]]:
    return dict(chat_id=chat, user_id=user)


class MongoStorage(BaseStorage):
    def __init__(
        self,
        mongo_client: AsyncIOMotorClient,
        mongo_database: AsyncIOMotorDatabase,
        collection_name: str = 'users'
    ) -> None:
        self.client = mongo_client
        self.database = mongo_database
        self.collection_name = collection_name
        self.db = addict.Dict(
            dict(users=self.database[collection_name])
        )

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
        chat: Optional[int] = None,
        user: Optional[int] = None,
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
        chat: Optional[int] = None,
        user: Optional[int] = None,
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
        chat: Optional[int] = None,
        user: Optional[int] = None,
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
        chat: Optional[int] = None,
        user: Optional[int] = None
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
    async def reset_data(self, *, chat: Optional[int] = None, user: Optional[int] = None) -> None:
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
    async def reset_state(self, *, chat: Optional[int] = None, user: Optional[int] = None) -> None:
        raise NotImplementedError

    @resolve_address
    async def finish(self, *, chat: Optional[int] = None, user: Optional[int] = None) -> None:
        raise NotImplementedError

    @resolve_address
    async def get_bucket(
        self,
        *,
        chat: Optional[int] = None,
        user: Optional[int] = None,
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
        chat: Optional[int] = None,
        user: Optional[int] = None,
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
        chat: Optional[int] = None,
        user: Optional[int] = None,
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
    async def reset_bucket(self, *, chat: Optional[int] = None, user: Optional[int] = None) -> None:
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
