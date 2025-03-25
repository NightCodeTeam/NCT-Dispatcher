import pytest


@pytest.mark.asyncio
async def test_post_incident(test_client, test_db):
    res = await test_client.post('/test')
    assert res.json().get('ok') == True