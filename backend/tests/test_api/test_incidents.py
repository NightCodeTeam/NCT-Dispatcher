import pytest

from httpx import AsyncClient
from src.database import Incident, DataBase
from core.sql_repository.exeptions import ItemNotFound


async def test_post_incident_success(test_client: AsyncClient):
    test_data = {
        'incident': {
            'title': 'Test Incident',
            'message': 'test message',
            'logs': 'log1\nlog2',
            'level': 'error',
        },
        'app_name': 'MainTestApp',
        'app_code': 'test_code_123',
    }
    data = await test_client.post(
        '/v1/incidents/new',
        json=test_data
    )
    assert data.status_code == 200
    assert data.json().get('ok') == True


async def test_post_incident_wrong_app(test_client: AsyncClient):
    test_data = {
        'incident': {
            'title': 'Test Incident',
            'message': 'test message',
            'logs': 'log1\nlog2',
            'level': 'error',
        },
        'app_name': 'NotExistedApp',
        'app_code': '12345',
    }
    data = await test_client.post(
        '/v1/incidents/new',
        json=test_data
    )
    assert data.status_code == 400


async def test_get_incident_info(test_client: AsyncClient, test_db: DataBase):
    test_inc = Incident(
        id=10,
        title='Test Incident',
        message='test message',
        logs='log1\nlog2',
        level='error',
        app_id=1,
    )

    test_db.session.add(test_inc)
    await test_db.commit()

    res = await test_client.get('/v1/incidents/10')
    assert res.status_code == 200
    assert res.json().get('title') == test_inc.title
    assert res.json().get('message') == test_inc.message
    assert res.json().get('logs') == test_inc.logs
    assert res.json().get('level') == test_inc.level
    assert res.json().get('app_name') == 'MainTestApp'


async def test_get_incident_info_wrong_id(test_client: AsyncClient):
    res = await test_client.get('/v1/incidents/100')
    assert res.status_code == 404


async def test_del_incident_success(test_client: AsyncClient, test_db: DataBase):
    test_inc = Incident(
        id=12,
        title='Test Incident',
        message='test message',
        logs='log1\nlog2',
        level='error',
        app_id=1,
    )
    test_db.session.add(test_inc)
    await test_db.commit()
    res = await test_client.delete('/v1/incidents/12')

    assert res.status_code == 200
    assert res.json().get('ok') is True
    assert await test_db.incidents.by_id(incident_id=12) is None


async def test_del_incident_success_wrong(test_client: AsyncClient, test_db: DataBase):
    try:
        res = await test_client.delete('/v1/incidents/120')
    except Exception as e:
        assert type(e) is ItemNotFound


async def test_update_status_success(test_client: AsyncClient, test_db: DataBase):
    test_inc = Incident(
        id=15,
        title='Test Incident',
        message='test message',
        logs='log1\nlog2',
        level='error',
        app_id=1,
    )
    test_db.session.add(test_inc)
    await test_db.commit()

    res = await test_client.put('/v1/incidents/15/status', json={
        'new_status': 'closed'
    })
    assert res.status_code == 200
    assert res.json().get('ok') is True


async def test_update_status_success_wrong_id(test_client: AsyncClient, test_db: DataBase):
    res = await test_client.put('/v1/incidents/150/status', json={
        'new_status': 'closed'
    })
    assert res.status_code == 404


async def test_all_incidents_success(test_client: AsyncClient, test_db: DataBase):
    await test_db.incidents.clear_table()
    test_inc_1 = Incident(
        id=17,
        title='Test Incident',
        message='test message',
        logs='log1\nlog2',
        level='error',
        app_id=1,
    )
    test_inc_2 = Incident(
        id=18,
        title='Test Incident',
        message='test message',
        logs='log1\nlog2',
        level='error',
        app_id=1,
    )
    test_db.session.add(test_inc_1)
    test_db.session.add(test_inc_2)
    await test_db.commit()

    res = await test_client.get('/v1/incidents')
    assert res.status_code == 200
    assert type(res.json().get('incidents')) is list
    assert len(res.json().get('incidents')) == 2
