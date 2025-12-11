from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.debug import logger
from core.trash import generate_trash_string
from database.models import App
from .base import Repository


class AppRepo(Repository):
    def __init__(self):
        super().__init__(App, ('incidents',))

    async def exists(self, app_id: int, session: AsyncSession) -> bool:
        return await self._exists(f"{self.table_name}.id={app_id}", session=session)

    async def by_id(self, app_id: int, session: AsyncSession, load_relations: bool = True) -> App | None:
        return await self.get(
            f"{self.table_name}.id={app_id}",
            session=session,
            load_relations=load_relations
        )

    async def by_name(self, name: str, session: AsyncSession, load_relations: bool = True) -> App | None:
        return await self.get(
            f"{self.table_name}.name='{name}'",
            session=session,
            load_relations=load_relations
        )

    async def by_name_code(
        self,
        name: str,
        code: str,
        session: AsyncSession,
        load_relations: bool = True
    ) -> App | None:
        return await self.get(
            f"{self.table_name}.name='{name}' AND {self.table_name}.code='{code}'",
            session=session,
            load_relations=load_relations
        )

    @staticmethod
    async def codes(session: AsyncSession) -> tuple[str, ...]:
        return tuple((await session.execute(select(App.code))).scalars().all())

    async def new(
        self,
        session: AsyncSession,
        name: str,
        added_by_id: int,
        status_url: str | None = None,
        logs_folder: str | None = None,
        commit: bool = True
    ) -> bool:
        return await self.add(App(
            name=name,
            code=generate_trash_string(20),
            status_url=status_url,
            logs_folder=logs_folder,
            added_by_id=added_by_id,
        ), session=session, commit=commit)

    async def del_by_id(
        self,
        app_id: int,
        session: AsyncSession,
        commit: bool = True
    ) -> bool:
        app = await self.by_id(app_id=app_id, session=session)
        if app:
            return await self.delete(obj=app, session=session, commit=commit)
        return False
