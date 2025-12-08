import pytest
from httpx import AsyncClient


async def test_post_incident(test_client: AsyncClient):
    data = await test_client.post('/incidents/new', json={
        'incident': {
            'title': 'Test 1',
            'message': 'Test incident message lorem',
            'logs': 'ERROR\t12:00\tTest error',
            'level': 'error',
        },
        'app_name': 'MainTestApp',
        'code': 'test_code_123'
    })
    assert data.status_code == 200
    assert data.json().get('ok') == True
