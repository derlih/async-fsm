import contextlib
import inspect
from abc import ABC, abstractmethod

from .is_cm import is_async_cm, is_cm


class State(ABC):
    @abstractmethod
    async def enter(self):  # pragma: no cover
        pass

    @abstractmethod
    async def exit(self):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def original_state(self):  # pragma: no cover
        pass


class StateContextManager(State):
    def __init__(self, cm):
        self._orig = cm
        self._cm = None

    async def enter(self):
        self._cm = self._orig()
        self._cm.__enter__()

    async def exit(self):
        self._cm.__exit__(None, None, None)

    @property
    def original_state(self):
        return self._orig


class StateCoroutineFunction(State):
    def __init__(self, coro):
        self._coro = coro

    async def enter(self):
        await self._coro()

    async def exit(self):
        pass

    @property
    def original_state(self):
        return self._coro


class StateAsyncContextManager(State):
    def __init__(self, cm):
        self._orig = cm
        self._cm = None

    async def enter(self):
        self._cm = self._orig()
        await self._cm.__aenter__()

    async def exit(self):
        await self._cm.__aexit__(None, None, None)

    @property
    def original_state(self):
        return self._orig


class StateFunction(State):
    def __init__(self, fn):
        self._fn = fn
        self._cm = None
        self._acm = None

    async def enter(self):
        res = self._fn()

        if is_cm(res):
            self._cm = res
            self._cm.__enter__()
        elif is_async_cm(res):
            self._acm = res
            await self._acm.__aenter__()

    async def exit(self):
        if self._cm:
            self._cm.__exit__(None, None, None)
            self._cm = None
        elif self._acm:
            await self._acm.__aexit__(None, None, None)
            self._acm = None

    @property
    def original_state(self):
        return self._fn
