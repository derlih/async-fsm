import asyncio
import contextlib
import inspect

from .exceptions import *
from .is_cm import is_async_cm, is_cm
from .state import (StateAsyncContextManager, StateContextManager,
                    StateCoroutineFunction, StateFunction)


class StateFactory:
    def create(self, obj):
        if inspect.isclass(obj) and is_cm(obj):
            return StateContextManager(obj)
        elif inspect.isclass(obj) and is_async_cm(obj):
            return StateAsyncContextManager(obj)
        elif asyncio.iscoroutinefunction(obj):
            return StateCoroutineFunction(obj)
        # NOTE: callable check should be the last one because
        # if class is passed by name, python threads its constructor as callable
        elif callable(obj):
            return StateFunction(obj)

        raise StateInvalidArgument('state is unsupported type')
