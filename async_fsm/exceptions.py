class BaseException(Exception):
    pass


class MachineInvalidConfiguration(BaseException):
    pass


class MachineWrongCreationParameters(MachineInvalidConfiguration):
    pass


class StateInvalidArgument(BaseException):
    pass
