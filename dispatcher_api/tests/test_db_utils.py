import pytest
from sqlalchemy.engine import create
from app.core.debug import create_log
from app.database.utils import (
    get_object_from_db,
    get_banned_ips_from_db,
    get_incidents_from_db,
    get_apps_from_db
)
from app.database.models import App, Incident, BannedIP


@pytest.mark.asyncio
async def test_get_object_from_db(test_db):
    test_db.add(
        App(name="Test App", url="http://test_app", dispatcher_code="123testcode")
    )
    await test_db.commit()

    obj = await get_object_from_db(App, 'apps.name = "Test App"', session = test_db)
    assert obj is not None
    assert obj[0].name == 'Test App'


    test_db.add(
        Incident(
            title="Test Incident",
            message="This is a test incident",
            logs='log1\nlog2',
            level='info',
            app_id=obj[0].id,
        )
    )
    await test_db.commit()

    obj = await get_object_from_db(Incident, 'incidents.title = "Test Incident" AND incidents.message = "This is a test incident"', session = test_db)

    assert obj is not None
    assert obj[0].title == 'Test Incident'
    assert obj[0].message == 'This is a test incident'
    assert obj[0].logs == 'log1\nlog2'
    assert obj[0].level == 'info'


@pytest.mark.asyncio
async def test_get_banned_ips_from_db(test_db):
    test_db.add(
        BannedIP(ip="192.168.1.1", reason="Test reason")
    )
    await test_db.commit()

    obj = await get_banned_ips_from_db('bannedips.ip = "192.168.1.1"', session = test_db)

    assert obj is not None
    assert obj[0].ip == '192.168.1.1'
    assert obj[0].reason == 'Test reason'


@pytest.mark.asyncio
async def test_get_apps_from_db(test_db):
    test_db.add(
        App(name="Test App", url="http://test_app", dispatcher_code="123testcode")
    )
    await test_db.commit()

    obj = await get_apps_from_db('apps.name = "Test App"', session = test_db)

    assert obj is not None
    assert obj[0].name == 'Test App'
    assert obj[0].url == 'http://test_app'
    assert obj[0].dispatcher_code == '123testcode'


@pytest.mark.asyncio
async def test_get_incidents_from_db(test_db):
    test_db.add(
        App(name="Test App", url="http://test_app", dispatcher_code="123testcode")
    )
    await test_db.commit()

    obj = await get_apps_from_db('apps.name = "Test App"', session = test_db)

    test_db.add(
        Incident(
            title="Test Incident",
            message="This is a test incident",
            logs='log1\nlog2',
            level='info',
            app_id=obj[0].id,
        )
    )
    await test_db.commit()

    obj = await get_incidents_from_db('incidents.title = "Test Incident" AND incidents.message = "This is a test incident"', session = test_db)

    assert obj is not None
    assert obj[0].title == 'Test Incident'
    assert obj[0].message == 'This is a test incident'
    assert obj[0].logs == 'log1\nlog2'
    assert obj[0].level == 'info'
