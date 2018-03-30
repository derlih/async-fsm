import asyncio
import contextlib

from .exceptions import *
from .state import *


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

        raise StateInvalidArgument('state is unsupported type')
