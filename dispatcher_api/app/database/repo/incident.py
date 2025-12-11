import logging
from sqlite3 import IntegrityError
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from database.models.incident import Incident
from .base import Repository


class IncidentRepo(Repository):
    def __init__(self):
        super().__init__(Incident, ('edit_by', 'app'))

    async def by_id(self, incident_id: int, session: AsyncSession | None = None) -> Incident | None:
        return await self.get(_filter=f'{self.table_name}.id={incident_id}', session=session)

    async def by_app_id(self, app_id: int, session: AsyncSession | None = None) -> tuple[Incident, ...]:
        return await self.some(f'{self.table_name}.app_id={app_id}', session=session)

    async def new(
        self,
        title: str,
        message: str,
        logs: str,
        level: str,
        app_id: int,
        session: AsyncSession,
        commit: bool = True
    ) -> bool:
        try:
            return await self.add(Incident(
                title=title,
                message=message,
                logs=logs,
                level=level,
                app_id=app_id,
            ), session=session, commit=commit)
        except IntegrityError:
            logging.error(f'Cant insert {title} exists')
            return False

    async def del_by_id(self, incident_id: int, session: AsyncSession, commit: bool = False) -> bool:
        data = await self.by_id(incident_id, session)
        if data:
            return await self.delete(data, session, commit)
        return False

    async def update_status(
        self,
        incident_id: int,
        new_status: Literal['open', 'closed'],
        session: AsyncSession,
        commit: bool = False
    ) -> bool:
        incident = await self.by_id(incident_id=incident_id, session=session)
        if incident:
            incident.status = new_status
            if commit:
                await session.commit()
            return True
        return False

    async def only_open(self, limit: int | None = None, session: AsyncSession | None = None):
        return await self.some(f"{self.table_name}.status='open'", limit=limit, session=session)

    async def only_closed(self, limit: int | None = None, session: AsyncSession | None = None):
        return await self.some(f"{self.table_name}.status='closed'", limit=limit, session=session)
