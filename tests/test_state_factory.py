import asyncio
from contextlib import contextmanager

import pytest
from async_fsm.exceptions import StateInvalidArgument
from async_fsm.state import *
from async_fsm.state_factory import StateFactory, is_async_cm, is_cm


@pytest.fixture
def factory():
    return StateFactory()


def test_create_from_unsupported_type(factory):
    with pytest.raises(StateInvalidArgument):
        factory.create('')


def fn():
    pass


@contextmanager
def cm_fn():
    yield


async def coro():
    pass


class CM:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, tb):
        pass


class AsyncCM:
    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_value, tb):
        pass


@pytest.mark.parametrize('obj,t', [
    (fn, StateFunction),
    (cm_fn, StateFunction),
    (CM, StateContextManager),
    (coro, StateCoroutineFunction),
    (AsyncCM, StateAsyncContextManager),
])
@pytest.mark.asyncio
async def test_create(factory, obj, t):
    s = factory.create(obj)
    assert isinstance(s, t)
    assert s.original_state is obj
    assert s.original_state is obj
