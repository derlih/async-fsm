from typing import NamedTuple

from .state import State


class Transition(NamedTuple):
    from_state: State
    to_state: State
    event: str
