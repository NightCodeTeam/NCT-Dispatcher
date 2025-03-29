import pytest

from app.core.single import Singleton


def test_single_instance():
    single = Singleton()
    assert single is Singleton()
