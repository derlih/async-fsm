import asyncio
from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest
from async_fsm.exceptions import *
from async_fsm.state import *


async def check_state(state, enter, exit):
    assert enter.call_count == 0
    assert exit.call_count == 0

    for x in range(1, 3):
        await state.enter()
        assert enter.call_count == x
        assert exit.call_count == x - 1

        await state.exit()
        assert enter.call_count == x
        assert exit.call_count == x


@pytest.mark.asyncio
async def test_sync_cm():
    enter = MagicMock()
    exit = MagicMock()

    @contextmanager
    def sync_state():
        enter()
        yield
        exit()

    s = StateContextManager(sync_state)
    await check_state(s, enter, exit)


@pytest.mark.asyncio
async def test_sync_cm_as_function():
    enter = MagicMock()
    exit = MagicMock()

    @contextmanager
    def sync_state():
        enter()
        yield
        exit()

    s = StateFunction(sync_state)
    await check_state(s, enter, exit)


@pytest.mark.asyncio
async def test_coroutine_function():
    enter = MagicMock()

    async def fn():
        enter()

    s = StateCoroutineFunction(fn)

    assert enter.call_count == 0

    await s.enter()
    enter.assert_called_once()

    await s.exit()


@pytest.mark.asyncio
async def test_async_cm():
    enter = MagicMock()
    exit = MagicMock()

    class AsyncCM:
        async def __aenter__(self):
            enter()

        async def __aexit__(self, exc_type, exc, tb):
            exit()

    s = StateAsyncContextManager(AsyncCM)
    await check_state(s, enter, exit)


@pytest.mark.asyncio
async def test_sync_function():
    enter = MagicMock()

    def fn():
        enter()

    s = StateFunction(fn)

    assert enter.call_count == 0

    await s.enter()
    enter.assert_called_once()

    await s.exit()


@pytest.mark.asyncio
async def test_sync_cm_function():
    enter = MagicMock()
    exit = MagicMock()
    cm = pytest.helpers.CM(enter, exit)

    def fn():
        return cm

    s = StateFunction(fn)
    await check_state(s, enter, exit)


@pytest.mark.asyncio
async def test_async_cm_function():
    enter = MagicMock()
    exit = MagicMock()
    cm = pytest.helpers.AsyncCM(enter, exit)

    def fn():
        return cm

    s = StateFunction(fn)
    await check_state(s, enter, exit)
