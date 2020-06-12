import asyncio
import typing

import aiogram
from aiogram.types import base
from aiogram import types


class Bot(aiogram.Bot):
    async def send_large_message(
        self,
        chat_id: typing.Union[base.Integer, base.String],
        text: base.String,
        disable_web_page_preview: typing.Optional[base.Boolean] = None,
        disable_notification: typing.Optional[base.Boolean] = None,
        reply_to_message_id: typing.Optional[base.Integer] = None,
        max_length: base.Integer = 4096
    ) -> typing.List[types.Message]:
        """No parse_mode is supported"""
        kwargs = locals()
        ignore_keys = (
            'self',
            'text',
            'max_length',
        )
        for key in ignore_keys:
            del kwargs[key]

        start_index = 0
        end_index = max_length
        cut_text = text[start_index:end_index]

        result_messages = []
        while cut_text:
            message = await self.send_message(text=cut_text, **kwargs)
            result_messages.append(message)
            start_index = end_index
            end_index += max_length
            cut_text = text[start_index:end_index]

        return result_messages

    async def send_with_action(
        self,
        chat_id: int,
        coroutine: typing.Awaitable,
        action: str = types.ChatActions.TYPING,
        delay: int = 5
    ) -> typing.Any:
        async def infinite_chat_action(tracked_task: asyncio.Task) -> None:
            while True:
                if tracked_task.done():
                    break
                else:
                    await self.send_chat_action(chat_id=chat_id, action=action)
                    await asyncio.sleep(delay)

        tracked_task = asyncio.create_task(coroutine)
        infinite_chat_action_task = asyncio.create_task(
            infinite_chat_action(tracked_task)
        )
        tasks = [infinite_chat_action_task, tracked_task]

        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        coro = next(iter(done))
        return coro.result()
