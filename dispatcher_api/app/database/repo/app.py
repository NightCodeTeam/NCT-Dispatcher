from sqlite3 import IntegrityError
from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from core import create_log
from database.models.app import App
from .base_repo import Repository


class AppRepo(Repository):
    def __init__(self):
        super().__init__(App)

    @override
    async def get(
        self,
        _filter: str,
        session: AsyncSession | None = None
    ) -> App | None:
        return await super().get(_filter=_filter, session=session)

    @override
    async def some(
        self,
        _filter: str,
        limit: int | None = None,
        session: AsyncSession | None = None
    ) -> tuple[App, ...] | None:
        return await super().some(_filter=_filter, session=session)

    @override
    async def add(self, obj: App, session: AsyncSession | None = None, commit: bool = False) -> bool:
        return await super().add(model=obj, session=session, commit=False)

    #async def update(self, obj: Type[T], session: AsyncSession | None) -> None:
    #    pass

    @override
    async def delete(self, obj: App, session: AsyncSession | None = None, commit: bool = False) -> bool:
        return await super().delete(obj=obj, session=session)

    @override
    async def all(self, limit: int | None = None, session: AsyncSession | None = None) -> tuple[App, ...]:
        return await super().all(limit=limit, session=session)

    async def get_app_by_id(self, app_id: int, session: AsyncSession | None = None) -> App | None:
        return await self.get(_filter=f'{self.table_name}.id={app_id}', session=session)

    async def get_app_by_ip_name_code(self, app_id: int, name: str, code: str, session: AsyncSession | None = None) -> App | None:
        return await self.get(
            _filter=f"{self.table_name}.id={app_id}"
                    f"AND {self.table_name}.name='{name}'"
                    f"AND {self.table_name}.dispatcher_code='{code}'",
            session=session
        )
    async def get_app_by_name_code(self, name: str, code: str, session: AsyncSession | None = None) -> App | None:
        return await self.get(
            _filter=f"{self.table_name}.name='{name}' "
                    f"AND {self.table_name}.dispatcher_code='{code}'",
            session=session
        )

    async def add_app(self, name: str, url: str, dispatcher_code: str, session: AsyncSession | None = None, commit: bool = False) -> bool:
        try:
            return await self.add(App(
                name=name,
                url=url,
                dispatcher_code=dispatcher_code
            ), session=session, commit=commit)
        except IntegrityError:
            create_log(f'Cant insert {name}: code {dispatcher_code} exists', 'error')
            return False

    async def delete_by_ip(self, app_id: int, session: AsyncSession | None = None, commit: bool = False) -> bool:
        data = await self.get_app_by_id(app_id, session)
        if data:
            return await self.delete(data, session, commit)
        return False
