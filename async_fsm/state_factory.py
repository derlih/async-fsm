import asyncio
import contextlib

from .exceptions import *
from .state import *


def is_async_cm(obj):
    return asyncio.iscoroutinefunction(getattr(obj, '__aenter__', None)) \
        and asyncio.iscoroutinefunction(getattr(obj, '__aexit__', None))


def is_cm(obj):
    return callable(getattr(obj, '__enter__', None)) \
        and callable(getattr(obj, '__exit__', None))


class StateFactory:
    def create(self, obj):
        if is_cm(obj):
            return StateContextManager(obj)
        elif is_async_cm(obj):
            return StateAsyncContextManager(obj)
        elif asyncio.iscoroutinefunction(obj):
            return StateCoroutineFunction(obj)
        elif asyncio.iscoroutine(obj):
            return StateCoroutineObject(obj)
        # NOTE: callable check should be the last one because
        # if class is passed by name, python threads its constructor as callable
        elif callable(obj):
            return StateFunction(obj)

        raise StateInvalidArgument('state is unsupported type')
