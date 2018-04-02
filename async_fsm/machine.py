import functools

from .exceptions import *
from .log import machine_logger
from .state_factory import StateFactory
from .transition import Transition


def check_configuration(states, transitions):
    machine_logger.debug('Check machine configuration')

    if not isinstance(states, set):
        err = 'states must be a set'
        machine_logger.error(err)
        raise MachineWrongCreationParameters(err)
    elif not states:
        err = 'states is empty'
        machine_logger.error(err)
        raise MachineWrongCreationParameters(err)
    if not isinstance(transitions, set):
        err = 'transitions must be a set'
        machine_logger.error(err)
        raise MachineWrongCreationParameters(err)
    elif not transitions:
        err = 'transitions is empty'
        machine_logger.error(err)
        raise MachineWrongCreationParameters(err)


class Machine:
    def __init__(self, state_factory, init_state, other_states, transitions):
        self._init_state = self._current_state = state_factory.create(
            init_state)
        self._states = [state_factory.create(s) for s in other_states]
        self._transitions = [self.create_transition(t) for t in transitions]

    def create_transition(self, transition):
        if transition[0] is self._init_state.original_state:
            from_state = self._init_state
        else:
            from_state = next(
                (s for s in self._states
                 if s.original_state is transition[0]))

        if transition[1] is self._init_state:
            to_state = self._init_state
        else:
            to_state = next(
                (s for s in self._states
                 if s.original_state is transition[1]))

        return Transition(from_state, to_state, transition[2])

    def __getattr__(self, attr):
        filtered_transitions = [
            t for t in self._transitions if t.event == attr]
        transition = next(
            (t for t in filtered_transitions
             if t.from_state is self._current_state), None)
        if not transition:
            async def noop():
                pass
            return noop

        async def coro():
            await transition.from_state.exit()
            self._current_state = transition.to_state
            await transition.to_state.enter()

        return coro


async def create_machine(init_state, other_states, transitions):
    m = Machine(StateFactory(), init_state, other_states, transitions)
    await m._current_state.enter()
    return m
