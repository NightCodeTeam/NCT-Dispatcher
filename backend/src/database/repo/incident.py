import logging
from datetime import datetime
from typing import Literal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.sql_repository import RepositoryObj, ItemNotFound
from src.database.models.incident import Incident


class IncidentRepo(RepositoryObj):
    def __init__(self, session: AsyncSession):
        super().__init__(Incident, session=session, relationships=('edit_by', 'app'))

    async def by_id(self, incident_id: int, load_relations: bool = True) -> Incident | None:
        return await self.get(
            filter_=Incident.id == incident_id,
            load_relations=load_relations,
        )

    async def by_app_id(self, app_id: int) -> tuple[Incident, ...]:
        return await self.some(Incident.id == app_id)

    async def new(
        self,
        title: str,
        message: str,
        logs: str,
        level: str,
        app_id: int,
        commit: bool = False
    ) -> bool:
        try:
            return await self.add(Incident(
                title=title,
                message=message,
                logs=logs,
                level=level,
                app_id=app_id,
            ), commit=commit)
        except IntegrityError:
            logging.error(f'Cant insert {title} exists')
            return False

    async def del_by_id(self, incident_id: int, commit: bool = False) -> bool:
        data = await self.by_id(incident_id)
        if data is None:
            raise ItemNotFound(Incident, 'id', incident_id)
        return await self.delete(data, commit=commit)

    async def update_status(
        self,
        incident_id: int,
        new_status: Literal['open', 'closed'],
        updated_by_id: int,
        commit: bool = False
    ) -> bool:
        incident = await self.by_id(incident_id=incident_id)
        if incident is None:
            raise ItemNotFound(Incident, 'id', incident_id)
        incident.status = new_status
        incident.edit_by_id = int(updated_by_id)
        incident.updated_at = datetime.now()
        if commit:
            await self.session.commit()
        return True

    async def only_open(self, limit: int | None = None):
        return await self.some(Incident.status == 'open', limit=limit)

    async def only_closed(self, limit: int | None = None):
        return await self.some(Incident.status == 'closed', limit=limit)

    async def pagination(self, skip: int, limit: int, load_relations: bool = False) -> tuple[Incident]:
        return await self._pagination(
            skip=skip,
            limit=limit,
            load_relations=load_relations,
            order_by_field='created_at',
        )
