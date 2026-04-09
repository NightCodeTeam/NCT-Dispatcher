import pytest

from app.core.single import Singleton


def test_single():
    class A(Singleton):
        test = 10

    class B(Singleton):
        test = 20

    a = A()
    b = A()

    assert a is b

    b.test = 20
    assert a.test == 20

    c = B()
    assert a is not c
    assert b is not c
