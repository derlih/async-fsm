import asyncio
from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest
from async_fsm.exceptions import *
from async_fsm.state import *

# @pytest.mark.asyncio
# async def test_sync_function():
#     enter = MagicMock()

#     def fn():
#         enter()

#     s = State(fn)

#     assert enter.call_count == 0

#     await s.enter()
#     enter.assert_called_once()

#     await s.exit()


@pytest.mark.asyncio
async def test_sync_cm():
    enter = MagicMock()
    exit = MagicMock()

    @contextmanager
    def sync_state():
        enter()
        yield
        exit()

    s = StateContextManager(sync_state())
    assert enter.call_count == 0

    await s.enter()
    enter.assert_called_once()

    await s.exit()
    exit.assert_called_once()


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
async def test_coroutine_object():
    enter = MagicMock()

    async def fn():
        enter()

    s = StateCoroutineObject(fn())

    assert enter.call_count == 0

    await s.enter()
    enter.assert_called_once()

    await s.exit()


@pytest.mark.asyncio
async def test_async_cm():
    enter = MagicMock()
    exit = MagicMock()

    class A:
        async def __aenter__(self):
            enter()

        async def __aexit__(self, exc_type, exc, tb):
            exit()

    s = StateAsyncContextManager(A())
    assert enter.call_count == 0

    await s.enter()
    enter.assert_called_once()

    await s.exit()
    exit.assert_called_once()
