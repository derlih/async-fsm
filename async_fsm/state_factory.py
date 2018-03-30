import asyncio
import contextlib
import inspect

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
        if callable(obj):
            return StateFunction(obj)
        elif is_cm(obj):
            if inspect.isclass(obj):
                return StateContextManager(obj())
            else:
                return StateContextManager(obj)
        elif asyncio.iscoroutinefunction(obj):
            return StateCoroutineFunction(obj)
        elif asyncio.iscoroutine(obj):
            return StateCoroutineObject(obj)
        elif is_async_cm(obj):
            if inspect.isclass(obj):
                return StateAsyncContextManager(obj())
            else:
                return StateAsyncContextManager(obj)

        raise StateInvalidArgument('state is unsupported type')
