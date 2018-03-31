from contextlib import contextmanager
from unittest.mock import MagicMock, create_autospec

import pytest
from async_fsm import create_machine
from async_fsm.exceptions import *
from async_fsm.machine import Machine, check_configuration, create_machine
from async_fsm.state import State
from async_fsm.state_factory import StateFactory


@pytest.mark.parametrize('states,transitions', [
    ([], None),
    (set(), None),
    ({lambda: None}, None),
    ({lambda: None}, set()),
])
def test_check_configuration(states, transitions):
    with pytest.raises(MachineWrongCreationParameters):
        check_configuration(states=states, transitions=transitions)


@pytest.fixture
def factory():
    return create_autospec(StateFactory, specset=True)


class MockState(State):
    def __init__(self, en, ex=None):
        self.en = en
        self.ex = ex if ex else MagicMock()

    async def enter(self):
        self.en()

    async def exit(self):
        self.ex()


@pytest.mark.asyncio
async def test_create_machine(factory):
    enter = MagicMock()
    factory.create.side_effect = [MockState(enter)]
    m = await create_machine(factory, enter, [], [])
    factory.create.assert_called_once_with(enter)
    enter.assert_called_once()


@pytest.fixture
def machine(event_loop, factory):
    init_enter = MagicMock()
    init_exit = MagicMock()
    enter = MagicMock()
    init_state = MockState(init_enter, init_exit)
    state = MockState(enter)

    def init_state_fn(): return None

    def state_fn(): return None

    factory.create.side_effect = [init_state, state]
    m = event_loop.run_until_complete(create_machine(factory, init_state_fn, [state_fn],
                                                     []))
    return m, init_exit, enter


@pytest.mark.asyncio
async def test_ignore_event(machine):
    m, init_exit, state_enter = machine
    await m.foo()
    assert init_exit.call_count == 0
    assert state_enter.call_count == 0
