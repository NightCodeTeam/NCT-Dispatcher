import pytest
from httpx import AsyncClient


async def test_test(test_client: AsyncClient):
    ans = await test_client.post('/v1/auth/test')
    assert ans.status_code == 200
    assert ans.json().get('ok') is True