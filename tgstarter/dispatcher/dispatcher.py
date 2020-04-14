import importlib
from typing import (
    Any,
    Callable,
    Iterator,
)
from pathlib import Path
import inspect
import functools

import aiogram

from ..utils.helper import function_fullname


def module_names(path: Path, suffix: str = '.py') -> Iterator[str]:
    suffix_length = len(suffix)
    for item in path.rglob(f'*{suffix}'):
        if item.is_file():
            parts = list(item.parts)
            parts[-1] = item.name[:-suffix_length]  # cut off suffix
            yield '.'.join(parts)


class Dispatcher(aiogram.Dispatcher):
    def __init__(self, states_dir: str, *args: Any, **kwargs: Any) -> None:
        self.__states_directory = states_dir
        super().__init__(*args, **kwargs)

    def __state_switcher(self, callback: Callable[..., Any]) -> Callable[..., Any]:

        @functools.wraps(callback)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            chat = aiogram.types.Chat.get_current()
            user = aiogram.types.User.get_current()  # NOTE: maybe not the best way
            result = await callback(*args, **kwargs)
            if inspect.iscoroutinefunction(result):
                state = function_fullname(result)
                await self.storage.set_state(user=user.id, chat=chat.id, state=state)

            return result

        return wrapper

    def __import_states(self) -> None:
        path = Path(self.__states_directory)
        for name in module_names(path):
            importlib.import_module(name=name)

    async def start_polling(self, *args: Any, **kwargs: Any) -> Any:
        self.__import_states()
        return await super().start_polling(*args, **kwargs)

    def state_handler(
        self,
        *args: Any,
        primary_state: bool = False,
        bound: Callable[..., Any] = aiogram.Dispatcher.message_handler,
        **kwargs: Any
    ) -> Callable[..., Any]:

        def wrapper(callback: Callable[..., Any]) -> Any:
            if bound == self.errors_handler:
                handler = bound(*args, **kwargs)
                return handler(callback)

            else:
                state = kwargs.pop('state', None)
                if state is None:
                    state = function_fullname(callback)
                else:
                    if inspect.iscoroutinefunction(state):
                        state = function_fullname(state)

                states = [state]

                callback = self.__state_switcher(callback)
                if primary_state:
                    states.append(None)

                result = None  # for a linter :)
                for state in states:
                    handler = bound(*args, state=state, **kwargs)
                    result = handler(callback)
                return result

        return wrapper

    def any_update_handler(self) -> Callable:
        def wrapper(callback: Callable) -> Callable:
            self.updates_handler.register(callback, index=0)
            return callback

        return wrapper
