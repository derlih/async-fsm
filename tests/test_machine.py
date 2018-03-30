import pytest
from async_fsm import Machine
from async_fsm import exceptions
from contextlib import contextmanager


@contextmanager
def state1():
    yield

    
@contextmanager
def state2():
    yield


@pytest.mark.parametrize('states,transitions',[
    ([], None),
    (set(), None),
    ({ state1 }, None),
    ({ state1 }, set()),
])
def test_init_wrong_params(states, transitions):
    with pytest.raises(exceptions.MachineWrongCreationParameters):
        Machine(states, transitions)

