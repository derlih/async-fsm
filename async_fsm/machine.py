import functools

from .exceptions import *
from .log import machine_logger


class Machine:
    def __init__(self, states, transitions):
        self.check_configuration(states, transitions)
        self._states = states
        self._transitions = transitions

    def check_configuration(self, states, transitions):
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

        def __getattr__(self, attr):
            pass
