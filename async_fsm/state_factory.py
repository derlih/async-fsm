import asyncio
import contextlib

from .exceptions import *
from .state import *


def is_async_cm_instance(obj):
    return asyncio.iscoroutinefunction(getattr(obj, '__aenter__', None)) \
        and asyncio.iscoroutinefunction(getattr(obj, '__aexit__', None))


class StateFactory:
    def create(self, obj):
        if callable(obj):
            return StateFunction(obj)
        elif isinstance(obj, contextlib.AbstractContextManager):
            return StateContextManager(obj)
        elif asyncio.iscoroutinefunction(obj):
            return StateCoroutineFunction(obj)
        elif asyncio.iscoroutine(obj):
            return StateCoroutineObject(obj)
        elif is_async_cm_instance(obj):
            return StateAsyncContextManager(obj)

        raise StateInvalidArgument('state is unsupported type')
