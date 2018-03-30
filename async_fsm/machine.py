import functools
from .exceptions import *
from .log import machine_logger


class Machine:
    def __init__(self, states, transitions):
        self._states = states
        self._transitions = transitions
        self.check_configuration()

    def check_configuration(self):
        machine_logger.debug('Check machine configuration')

        if not isinstance(self._states, set):
            err = 'states must be a set'
            machine_logger.error(err)
            raise MachineWrongCreationParameters(err)
        elif not self._states:
            err = 'states is empty'
            machine_logger.error(err)
            raise MachineWrongCreationParameters(err)
        if not isinstance(self._transitions, set):
            err = 'transitions must be a set'
            machine_logger.error(err)
            raise MachineWrongCreationParameters(err)
        elif not self._transitions:
            err = 'transitions is empty'
            machine_logger.error(err)
            raise MachineWrongCreationParameters(err)
