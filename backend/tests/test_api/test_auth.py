import pytest


async def test_login(test_client):
    ans = await test_client.post('/v1/auth/login', json={
        'username': 'test', 'password': '123456'
    })
    assert ans.status_code == 200
    assert ans.json().get('access_token') is not None
    assert ans.json().get('token_type') == 'Bearer'


async def test_login_wrong(test_client):
    ans = await test_client.post('/v1/auth/login', json={
        'username': 'test123', 'password': '123456123'
    })
    assert ans.status_code == 401
    assert ans.json().get('access_token') is None
    assert ans.json().get('token_type') is None
