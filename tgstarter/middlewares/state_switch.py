from typing import List, Any

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import BaseStorage
from aiogram.types import Update, User, Chat


class StateSwitch(BaseMiddleware):
    def __init__(self, storage: BaseStorage) -> None:
        super(StateSwitch, self).__init__()
        self.storage = storage

    async def on_post_process_update(self, update: Update, results: List[Any], data: dict):
        handler_results, *_ = results
        try:
            last_handler_result = handler_results[-1]
        except IndexError:
            pass
        else:
            if isinstance(last_handler_result, str):
                user = User.get_current()
                chat = Chat.get_current()
                await self.storage.set_state(user=user.id, chat=chat.id, state=last_handler_result)
