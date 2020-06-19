import importlib
from typing import (
    Any,
    Callable,
    Iterator,
    Union,
    Optional,
)
from pathlib import Path
import inspect
import functools

import aiogram

from ..utils.helper import function_fullname
from tgstarter.utils.typing import AsyncCallbackVar, Handler


def module_names(path: Path, suffix: str = '.py') -> Iterator[str]:
    suffix_length = len(suffix)
    for item in path.rglob(f'*{suffix}'):
        if item.is_file():
            parts = list(item.parts)
            parts[-1] = item.name[:-suffix_length]  # cut off suffix
            yield '.'.join(parts)


class Dispatcher(aiogram.Dispatcher):
    def __init__(
        self,
        *args: Any,
        states_dir: str,
        **kwargs: Any
    ) -> None:
        self.__states_directory = states_dir
        super().__init__(*args, **kwargs)

    def __state_switcher(self, callback: AsyncCallbackVar) -> AsyncCallbackVar:

        @functools.wraps(callback)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            chat = aiogram.types.Chat.get_current()
            user = aiogram.types.User.get_current()  # NOTE: maybe not the best way
            result = await callback(*args, **kwargs)
            if isinstance(result, str):
                await self.storage.set_state(user=user.id, chat=chat.id, state=result)

            return result

        return wrapper

    def import_states(self) -> None:
        path = Path(self.__states_directory)
        for name in module_names(path):
            importlib.import_module(name=name)

    def state_handler(
        self,
        *args: Any,
        primary_state: bool = False,
        bound: Handler = aiogram.Dispatcher.message_handler,
        state: Optional[Union[str, Callable]] = None,
        **kwargs: Any
    ) -> Callable[[AsyncCallbackVar], Any]:

        def wrapper(callback: AsyncCallbackVar) -> AsyncCallbackVar:
            if bound == self.errors_handler:
                handler = bound(*args, **kwargs)
                return handler(callback)
            else:
                wrapped_callback = self.__state_switcher(callback)
                states = [state, None] if primary_state and state else [state]
                for state_ in states:
                    handler = bound(*args, state=state_, **kwargs)
                    handler(wrapped_callback)
                return callback

        return wrapper

    def any_update_handler(self) -> Callable[[AsyncCallbackVar], AsyncCallbackVar]:
        def wrapper(callback: AsyncCallbackVar) -> AsyncCallbackVar:
            self.updates_handler.register(callback, index=0)
            return callback

        return wrapper
