import pytest

from src.database import DataBase, Incident
from core.sql_repository.exeptions import ItemNotFound


async def test_all_empty(test_db: DataBase):
	await test_db.incidents.clear_table()

	inc = await test_db.incidents.all()
	assert len(inc) == 0


async def test_new_all(test_db: DataBase):
	await test_db.incidents.clear_table()

	ans = await test_db.incidents.new(
		title='Test Incident',
		message='test message',
		logs='log1\nlog2\nlog3',
		level='error',
		app_id=1,
	)
	assert ans is True

	incidents = await test_db.incidents.all()
	assert len(incidents) == 1
	assert incidents[0].title == 'Test Incident'
	assert incidents[0].message == 'test message'
	assert incidents[0].logs == 'log1\nlog2\nlog3'
	assert incidents[0].level == 'error'
	assert incidents[0].app_id == 1


async def test_by_id(test_db: DataBase):
	incident = await test_db.incidents.by_id(incident_id=1)
	assert incident is not None
	assert incident.id == 1
	assert incident.title == 'Test Incident'
	assert incident.message == 'test message'
	assert incident.logs == 'log1\nlog2\nlog3'
	assert incident.level == 'error'
	assert incident.app_id == 1


async def test_by_id_wrong(test_db: DataBase):
	ans = await test_db.incidents.by_id(incident_id=12345)
	assert ans is None


async def test_del_by_id(test_db: DataBase):
	ans = await test_db.incidents.del_by_id(
		incident_id=1,
		commit=True,
	)
	assert ans is True


async def test_del_by_id_wrong(test_db: DataBase):
	try:
		ans = await test_db.incidents.del_by_id(
			incident_id=5678,
		)
		assert False
	except ItemNotFound:
		assert True


async def test_update_status(test_db: DataBase):
    await test_db.incidents.new(
		title='Test Incident',
		message='test message',
		logs='log1\nlog2\nlog3',
		level='error',
		app_id=1,
	)
    await test_db.flush()

    ans = await test_db.incidents.update_status(
        incident_id=1,
        new_status='closed',
        updated_by_id=1,
        commit=True,
    )
    assert ans is True

    inc = await test_db.incidents.by_id(incident_id=1)

    assert inc is not None
    assert inc.status == 'closed'

    await test_db.incidents.del_by_id(
        incident_id=1,
        commit=True,
    )

async def test_only_open_close(test_db: DataBase):
	await test_db.incidents.clear_table()

	a = Incident(
		id=4,
		title='Test Incident',
		message='test message',
		logs='log1\nlog2\nlog3',
		level='error',
		app_id=1,
	)
	b = Incident(
		id=5,
		title='Test Incident',
		message='test message',
		logs='log1\nlog2\nlog3',
		level='error',
		status='closed',
		app_id=1,
	)
	test_db.session.add(a)
	test_db.session.add(b)

	await test_db.commit()

	ans = await test_db.incidents.only_open()
	assert len(ans) == 1

	ans = await test_db.incidents.only_closed()
	assert len(ans) == 1

	await test_db.incidents.clear_table()
