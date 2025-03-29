import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import App, Incident, BannedIP


@pytest.mark.asyncio
async def test_post_incident(test_client: AsyncClient, test_db: AsyncSession):
    test_db.add(
        App(name="Test App", url="http://test_app", dispatcher_code="123testcode")
    )
    await test_db.commit()
    res = await test_client.post('incidents/post_incident', json={
        'title': 'Test Incident',
        'message': 'Test router correct post',
        'level': 'info',
        'logs': 'some errror\nsome log',
        'app_name': 'Test App'
    }, headers={
        'Content-Type': 'application/json',
        'dispatch': '123testcode',
    })
    assert res.json().get('ok') == True
    assert (await test_db.execute(
        select(Incident).where(Incident.title == 'Test Incident')
    )).scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_post_wrong_incident(test_client: AsyncClient, test_db: AsyncSession):
    test_db.add(
        App(name="Test App", url="http://test_app", dispatcher_code="123testcode")
    )
    await test_db.commit()
    res = await test_client.post('incidents/post_incident', json={
        'title': 'Test Incident',
        'message': 'Test router correct post',
        'level': 'info',
        'logs': 'some errror\nsome log',
        'app_name': 'Test App'
    }, headers={
        'Content-Type': 'application/json',
        'dispatch': 'wrong-test-code',
    })
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_post_incident_wrong_app(test_client: AsyncClient, test_db: AsyncSession):
    test_db.add(
            App(name="Test App", url="http://test_app", dispatcher_code="123testcode")
        )
    await test_db.commit()
    res = await test_client.post('incidents/post_incident', json={
        'title': 'Test Incident',
        'message': 'Test router correct post',
        'level': 'info',
        'logs': 'some errror\nsome log',
        'app_name': 'Wrong App'
    }, headers={
        'Content-Type': 'application/json',
        'dispatch': '123testcode',
    })
    assert res.status_code == 404
    assert (await test_db.execute(
        select(BannedIP).where(BannedIP.ip == '127.0.0.1')
    )).scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_post_incident_no_dispatch(test_client: AsyncClient, test_db: AsyncSession):
    res = await test_client.post('incidents/post_incident', json={
        'title': 'Test Incident',
        'message': 'Test router correct post',
        'level': 'info',
        'logs': 'some errror\nsome log',
        'app_name': 'Test App'
    }, headers={
        'Content-Type': 'application/json',
    })
    assert res.status_code == 404
    assert (await test_db.execute(
        select(BannedIP).where(BannedIP.ip == '127.0.0.1')
    )).scalar_one_or_none() is not None

