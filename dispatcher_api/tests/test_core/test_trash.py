import pytest
from app.core.trash import generate_trash_string, \
    generate_unique_trash_string, UniqueGenerationFailed


def test_unique_generation():
    vals = [generate_trash_string(10) for _ in range(100)]
    try:
        st = generate_unique_trash_string(10, vals)
        assert type(st) is str
        assert len(st) == 10
        assert True
    except UniqueGenerationFailed:
        assert False
