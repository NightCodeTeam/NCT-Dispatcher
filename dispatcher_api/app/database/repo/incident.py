from sqlite3 import IntegrityError
from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from core import create_log
from database.models.incident import Incident
from .base_repo import Repository


class IncidentRepo(Repository):
    def __init__(self):
        super().__init__(Incident)

    @override
    async def get(
        self,
        _filter: str,
        session: AsyncSession | None = None
    ) -> Incident | None:
        return await super().get(_filter=_filter, session=session)

    @override
    async def some(
        self,
        _filter: str,
        limit: int | None = None,
        session: AsyncSession | None = None
    ) -> tuple[Incident, ...] | None:
        return await super().some(_filter=_filter, session=session)

    @override
    async def add(self, obj: Incident, session: AsyncSession | None = None, commit: bool = False) -> bool:
        return await super().add(model=obj, session=session, commit=False)

    #async def update(self, obj: Type[T], session: AsyncSession | None) -> None:
    #    pass

    @override
    async def delete(self, obj: Incident, session: AsyncSession | None = None, commit: bool = False) -> bool:
        return await super().delete(obj=obj, session=session)

    @override
    async def all(self, limit: int | None = None, session: AsyncSession | None = None) -> tuple[Incident, ...]:
        return await super().all(limit=limit, session=session)

    async def get_incident_by_id(self, incident_id: int, session: AsyncSession | None = None) -> Incident | None:
        return await self.get(_filter=f'{self.table_name}.id={incident_id}', session=session)

    async def add_incident(
            self,
            title: str,
            message: str,
            logs: str,
            level: str,
            status: str,
            app_id: int,
            session: AsyncSession,
            commit: bool = False
    ) -> bool:
        try:
            return await self.add(Incident(
                title=title,
                message=message,
                logs=logs,
                level=level,
                status=status,
                app_id=app_id,
            ), session=session, commit=commit)
        except IntegrityError:
            create_log(f'Cant insert {title} exists', 'error')
            return False

    async def delete_by_id(self, incident_id: int, session: AsyncSession, commit: bool = False) -> bool:
        data = await self.get_incident_by_id(incident_id, session)
        if data:
            return await self.delete(data, session, commit)
        return False

    async def get_by_app_id(self, app_id: int, session: AsyncSession | None = None) -> tuple[Incident, ...]:
        return await self.some(f'{self.table_name}.app_id={app_id}', session=session)

    async def only_open(self, limit: int | None = None, session: AsyncSession | None = None):
        return await self.some(f"{self.table_name}.status='open'", limit=limit, session=session)