import pytest

from database import DB, App


async def test_all_apps(test_client, test_db):
    data = await test_client.get('/v1/apps/')
    assert data.status_code == 200
    assert len(data.json().get('apps')) == 1
    assert data.json().get('apps')[0].get('name') == 'MainTestApp'


#async def test_new_success(test_client, test_db):
#    res = await test_client.post('/v1/apps/new', json={
#        'name': 'NewApp',
#        'status_url': '1',
#        'logs_folder': '2',
#    })
#    assert res.status_code == 200
#    assert res.json().get('ok') is True
#
#    data = await DB.apps.by_name('NewApp', session=test_db)
#    assert data is not None
#    assert data.name == 'NewApp'
#    assert data.status_url == '1'
#    assert data.logs_folder == '2'


async def test_app_by_id(test_client, test_db):
    res = await test_client.get('/v1/apps/1')
    assert res.status_code == 200
    assert res.json().get('name') == 'MainTestApp'
    assert res.json().get('status_url') == '-'


async def test_app_by_id_wrong_id(test_client, test_db):
    res = await test_client.get('/v1/apps/10')
    assert res.status_code == 404


async def test_app_logs(test_client, test_db):
    res = await test_client.get('/v1/apps/1/logs')
    assert res.status_code == 200
    assert type(res.json().get('logs')) is list


async def test_app_logs_wrong(test_client, test_db):
    res = await test_client.get('/v1/apps/100/logs')
    assert res.status_code == 404


async def test_del_app(test_client, test_db):
    app = App(
        id=16,
        name='DeleteApp',
        code='123',
        status_url='-',
        logs_folder='-',
        added_by_id=1,
    )
    test_db.add(app)
    await test_db.commit()

    res = await test_client.delete('/v1/apps/16')
    assert res.status_code == 200


async def test_del_app_wrong(test_client, test_db):
    res = await test_client.delete('/v1/apps/160')
    assert res.status_code == 404
