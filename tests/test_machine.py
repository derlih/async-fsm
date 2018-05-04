from contextlib import contextmanager
from unittest.mock import MagicMock, create_autospec

import pytest
from async_fsm import create_machine
from async_fsm.exceptions import *
from async_fsm.machine import Machine, check_configuration
from async_fsm.state import State
from async_fsm.state_factory import StateFactory


@pytest.mark.parametrize('states,transitions', [
    ([], None),
    (set(), None),
    (set([lambda: None]), None),
    (set([lambda: None]), set()),
])
def test_check_configuration(states, transitions):
    with pytest.raises(MachineWrongCreationParameters):
        check_configuration(states=states, transitions=transitions)


@pytest.fixture
def state_to_check_enter():
    state_enter = MagicMock()

    def state():
        state_enter()

    return state, state_enter


@pytest.mark.asyncio
async def test_create_machine(state_to_check_enter):
    init_state, init_state_enter = state_to_check_enter
    m = await create_machine(init_state, [], [])
    init_state_enter.assert_called_once()


@pytest.fixture
def state_to_check_exit():
    state_exit = MagicMock()

    @contextmanager
    def state():
        yield
        state_exit()

    return state, state_exit


@pytest.mark.asyncio
async def test_ignore_event(state_to_check_enter, state_to_check_exit):
    init_state, init_exit = state_to_check_exit
    another_state, another_state_enter = state_to_check_enter

    machine = await create_machine(init_state, [another_state], [])
    await machine.foo()
    assert init_exit.call_count == 0
    assert another_state_enter.call_count == 0


@pytest.mark.asyncio
async def test_transition_on_event(state_to_check_enter, state_to_check_exit):
    init_state, init_exit = state_to_check_exit
    another_state, another_state_enter = state_to_check_enter

    machine = await create_machine(init_state, [another_state], [
        (init_state, another_state, 'foo')
    ])
    await machine.foo()
    assert init_exit.call_count == 1
    assert another_state_enter.call_count == 1
