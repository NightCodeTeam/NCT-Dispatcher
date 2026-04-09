from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.debug import logger
from src.core.trash import generate_trash_string
from src.core.sql_repository import Repository, ItemNotFound
from database.models import App


class AppRepo(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(App, session=session, relationships=('incidents',))

    async def exists(self, app_id: int) -> bool:
        return await self._exists(f"{self.table_name}.id={app_id}")

    async def by_id(self, app_id: int, load_relations: bool = True) -> App | None:
        return await self.get(
            f"{self.table_name}.id={app_id}",
            load_relations=load_relations
        )

    async def by_name(self, name: str, load_relations: bool = True) -> App | None:
        return await self.get(
            f"{self.table_name}.name='{name}'",
            load_relations=load_relations
        )

    async def by_name_code(
        self,
        name: str,
        code: str,
        load_relations: bool = True
    ) -> App | None:
        return await self.get(
            f"{self.table_name}.name='{name}' AND {self.table_name}.code='{code}'",
            load_relations=load_relations
        )

    async def codes(self) -> tuple[str, ...]:
        return tuple((await self.session.execute(select(App.code))).scalars().all())

    async def new(
        self,
        name: str,
        added_by_id: int,
        status_url: str | None = None,
        logs_folder: str | None = None,
        commit: bool = False
    ) -> bool:
        return await self.add(App(
            name=name,
            code=generate_trash_string(20),
            status_url=status_url,
            logs_folder=logs_folder,
            added_by_id=added_by_id,
        ), commit=commit)

    async def del_by_id(
        self,
        app_id: int,
        commit: bool = False
    ) -> bool:
        app = await self.by_id(app_id=app_id)
        if app is None:
            raise ItemNotFound(App, 'id', app_id)
        return await self.delete(obj=app, commit=commit)

    async def pagination(self, skip: int, limit: int, load_relations: bool = False) -> tuple[App, ...]:
        return await super()._pagination(
            skip=skip,
            limit=limit,
            load_relations=load_relations,
            order_by_field='id'
        )
