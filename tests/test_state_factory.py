import asyncio
from contextlib import contextmanager

import pytest
from async_fsm.exceptions import *
from async_fsm.state import State
from async_fsm.state_factory import StateFactory


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
    pass


class CM:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, tb):
        pass


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
    fn,
    cm_fn, cm_fn(), CM(), CM,
    coro, coro_obj,
    AsyncCM(), AsyncCM,
])
def test_create(factory, obj):
    assert isinstance(factory.create(obj), State)
