from typing import Callable

import aiogram

from tgstarter.utils.typing import AsyncCallbackVar


class Dispatcher(aiogram.Dispatcher):
    def any_update_handler(self) -> Callable[[AsyncCallbackVar], AsyncCallbackVar]:
        def wrapper(callback: AsyncCallbackVar) -> AsyncCallbackVar:
            self.updates_handler.register(callback, index=0)
            return callback

        return wrapper
