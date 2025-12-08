import pytest
from httpx import AsyncClient


async def test_all_apps(test_client: AsyncClient):
    data = await test_client.get('/apps/')
    assert data.status_code == 200
    print(data)
    assert len(data.json().get('apps')) == 1
