import contextlib
from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    async def enter(self):
        pass

    @abstractmethod
    async def exit(self):
        pass


class StateContextManager(State):
    def __init__(self, cm):
        self._cm = cm

    async def enter(self):
        self._cm.__enter__()

    async def exit(self):
        self._cm.__exit__(None, None, None)


class StateCoroutineFunction(State):
    def __init__(self, coro):
        self._coro = coro

    async def enter(self):
        await self._coro()

    async def exit(self):
        pass


class StateCoroutineObject(State):
    def __init__(self, coro_obj):
        self._coro_obj = coro_obj

    async def enter(self):
        await self._coro_obj

    async def exit(self):
        pass


class StateAsyncContextManager(State):
    def __init__(self, cm):
        self._cm = cm

    async def enter(self):
        await self._cm.__aenter__()

    async def exit(self):
        await self._cm.__aexit__(None, None, None)


class StateFunction(State):
    def __init__(self, fn):
        self._fn = fn

    async def enter(self):
        res = self._fn()

        if isinstance(res, contextlib.AbstractContextManager):
            self._cm = res
            self.__class__ = StateContextManager
            self._cm.__enter__()

    async def exit(self):
        pass
