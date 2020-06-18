import abc
from typing import Generator, Any


class Handler:
    def __init__(self, event: Any) -> None:
        self.event = event

    def __await__(self) -> Generator:
        coroutine = self.handle(self.event)
        return coroutine.__await__()

    @abc.abstractmethod
    async def handle(self, event: Any):
        raise NotImplementedError('handle method must be implemented')
