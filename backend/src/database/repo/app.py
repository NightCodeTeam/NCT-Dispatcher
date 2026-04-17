from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.trash import generate_trash_string
from core.sql_repository import RepositoryObj, ItemNotFound
from src.database.models import App


class AppRepo(RepositoryObj):
    def __init__(self, session: AsyncSession):
        super().__init__(App, session=session, relationships=('incidents',))

    @staticmethod
    def generate_code() -> str:
        return generate_trash_string(20)

    async def exists(self, app_id: int) -> bool:
        return await self._exists(App.id == app_id)

    async def by_id(self, app_id: int, load_relations: bool = True) -> App | None:
        return await self.get(
            App.id == app_id,
            load_relations=load_relations
        )

    async def by_name(self, name: str, load_relations: bool = True) -> App | None:
        return await self.get(
            App.name == name,
            load_relations=load_relations
        )

    async def by_name_code(
        self,
        name: str,
        code: str,
        load_relations: bool = True
    ) -> App | None:
        return await self.get(
            and_(App.name == name, App.code == code),
            load_relations=load_relations
        )

    async def codes(self) -> tuple[str, ...]:
        return tuple((await self.session.execute(select(App.code))).scalars().all())

    async def new(
        self,
        name: str,
        added_by_id: int,
        status_url: str | None = None,
        status_code: str | None = None,
        logs_folder: str | None = None,
        script_path: str | None = None,
        commit: bool = False
    ) -> bool:
        return await self.add(App(
            name=name,
            code=self.generate_code(),
            status_url=status_url,
            status_code=status_code,
            logs_folder=logs_folder,
            script_path=script_path,
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
