pytest_plugins = ['helpers_namespace']

import pytest


@pytest.helpers.register
class CM:
    def __init__(self, enter=None, exit=None):
        self.enter = enter
        self.exit = exit

    def __enter__(self):
        if self.enter:
            self.enter()

    def __exit__(self, exc_type, exc_value, tb):
        if self.exit:
            self.exit()


@pytest.helpers.register
class AsyncCM:
    def __init__(self, enter=None, exit=None):
        self.enter = enter
        self.exit = exit

    async def __aenter__(self):
        if self.enter:
            self.enter()

    async def __aexit__(self, exc_type, exc_value, tb):
        if self.exit:
            self.exit()
