import pytest
from async_fsm.is_cm import is_async_cm, is_cm


def test_is_cm():
    assert is_cm(pytest.helpers.CM)


def test_is_async_cm():
    assert is_async_cm(pytest.helpers.AsyncCM)
