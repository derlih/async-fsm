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


class CM:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, tb):
        pass


@pytest.mark.parametrize('obj', [
    CM(), CM
])
def test_is_cm(obj):
    assert is_cm(obj)


async def coro():
    pass

coro_obj = coro()
# To remove asyncio warning
asyncio.ensure_future(coro_obj)


class AsyncCM:
    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_value, tb):
        pass


@pytest.mark.parametrize('obj', [
    AsyncCM(), AsyncCM
])
def test_is_async_cm(obj):
    assert is_async_cm(obj)


@pytest.mark.parametrize('obj,t', [
    (fn, StateFunction),
    (cm_fn, StateFunction),
    (cm_fn(), StateContextManager),
    (CM(), StateContextManager),
    (CM, StateContextManager),
    (coro, StateCoroutineFunction),
    (coro_obj, StateCoroutineObject),
    (AsyncCM(), StateAsyncContextManager),
    (AsyncCM, StateAsyncContextManager),
])
@pytest.mark.asyncio
async def test_create(factory, obj, t):
    s = factory.create(obj)
    assert isinstance(s, t)
    assert s.original_state is obj

    # await s.enter()
    # assert s.original_state is obj
