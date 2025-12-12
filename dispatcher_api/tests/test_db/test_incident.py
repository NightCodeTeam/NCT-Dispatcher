import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import DB, Incident
from app.database.repo.base import ItemNotFound


async def test_all_empty(test_db: AsyncSession):
	await DB.incidents.clear_table(session=test_db)

	inc = await DB.incidents.all(session=test_db)
	assert len(inc) == 0


async def test_new_all(test_db: AsyncSession):
	await DB.incidents.clear_table(session=test_db)

	ans = await DB.incidents.new(
		title='Test Incident',
		message='test message',
		logs='log1\nlog2\nlog3',
		level='error',
		app_id=1,
		session=test_db
	)
	assert ans is True

	incidents = await DB.incidents.all(
		session=test_db
	)
	assert len(incidents) == 1
	assert incidents[0].title == 'Test Incident'
	assert incidents[0].message == 'test message'
	assert incidents[0].logs == 'log1\nlog2\nlog3'
	assert incidents[0].level == 'error'
	assert incidents[0].app_id == 1

	ans = await DB.incidents.del_by_id(
		incident_id=incidents[0].id,
		session=test_db,
		commit=True
	)


async def test_by_id(test_db: AsyncSession):
	test = Incident(
		id=2,
		title='Test incident',
		message='test message2',
		logs='log4\nlog2\nlog3',
		level='debug',
		app_id=1,
	)
	test_db.add(test)
	await test_db.commit()

	incident = await DB.incidents.by_id(
		incident_id=2,
		session=test_db,
	)
	assert incident is not None
	assert incident.id == 2
	assert incident.title == 'Test incident'
	assert incident.message == 'test message2'
	assert incident.logs == 'log4\nlog2\nlog3'
	assert incident.level == 'debug'
	assert incident.app_id == 1

	ans = await DB.incidents.del_by_id(
		incident_id=2,
		session=test_db,
		commit=True
	)


async def test_by_id_wrong(test_db: AsyncSession):
	ans = await DB.incidents.by_id(
		incident_id=12345,
		session=test_db,
	)
	assert ans is None


async def test_del_by_id(test_db: AsyncSession):
	test_db.add(Incident(
		id=23456,
		title='123',
		message='test',
		logs='-',
		level='debug',
		app_id=1,
	))
	await test_db.commit()

	ans = await DB.incidents.del_by_id(
		incident_id=23456,
		session=test_db,
		commit=True,
	)

	assert ans is True


async def test_del_by_id_wrong(test_db: AsyncSession):
	try:
		ans = await DB.incidents.del_by_id(
			incident_id=5678,
			session=test_db,
			commit=True
		)
		assert False
	except Exception as e:
		assert type(e) is ItemNotFound


async def test_update_status(test_db: AsyncSession):
	test_db.add(Incident(
		id=3,
		title='Test Incident',
		message='test message',
		logs='log1\nlog2\nlog3',
		level='error',
		app_id=1,
	))
	await test_db.commit()

	ans = await DB.incidents.update_status(
		incident_id=3,
		new_status='closed',
		session=test_db,
	)

	assert ans is True

	inc = await DB.incidents.by_id(
		incident_id=3,
		session=test_db
	)

	assert inc is not None
	assert inc.status == 'closed'

	await DB.incidents.del_by_id(
		incident_id=3,
		session=test_db,
		commit=True,
	)

async def test_only_open_close(test_db: AsyncSession):
	await DB.incidents.clear_table(session=test_db)

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
	test_db.add(a)
	test_db.add(b)

	await test_db.commit()

	ans = await DB.incidents.only_open(session=test_db)
	assert len(ans) == 1

	ans = await DB.incidents.only_closed(session=test_db)
	assert len(ans) == 1

	await test_db.delete(a)
	await test_db.delete(b)
	await test_db.commit()
