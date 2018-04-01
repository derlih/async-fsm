import contextlib
import inspect
from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    async def enter(self):
        pass

    @abstractmethod
    async def exit(self):
        pass

    @property
    @abstractmethod
    def original_state(self):
        pass


class StateContextManager(State):
    def __init__(self, cm):
        self._orig = cm
        if inspect.isclass(cm):
            self._cm = cm()
        else:
            self._cm = cm

    async def enter(self):
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


class StateCoroutineObject(State):
    def __init__(self, coro_obj):
        self._coro_obj = coro_obj

    async def enter(self):
        await self._coro_obj

    async def exit(self):
        pass

    @property
    def original_state(self):
        return self._coro_obj


class StateAsyncContextManager(State):
    def __init__(self, cm):
        self._orig = cm
        if inspect.isclass(cm):
            self._cm = cm()
        else:
            self._cm = cm

    async def enter(self):
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

    async def enter(self):
        res = self._fn()

        if isinstance(res, contextlib.AbstractContextManager):
            self._cm = res
            self._cm.__enter__()

    async def exit(self):
        if self._cm:
            self._cm.__exit__(None, None, None)

    @property
    def original_state(self):
        return self._fn
