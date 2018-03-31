from typing import NamedTuple


class Transition(NamedTuple):
    from_state: object
    to_state: object
    event: str
