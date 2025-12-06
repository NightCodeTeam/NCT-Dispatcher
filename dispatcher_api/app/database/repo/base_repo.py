from abc import ABC, abstractmethod
from typing import TypeVar, Type
from sqlalchemy import text, select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.debug import create_log
from core.single import Singleton
from database.database import Base
from database.session import new_session


T = TypeVar('T', bound=Base)


class Repository(ABC, Singleton):
    table_name: str

    def __init__(self, model: Type[T]):
        self.model = model
        self.table_name = model.__tablename__

    async def __get_object_from_db(
        self,
        _filter: str | None = None,
        limit: int | None = None,
        session: AsyncSession | None = None
    ) -> tuple[T, ...]:
        if _filter is not None:
            query = select(self.model).filter(text(_filter))
        else:
            query = select(self.model)
        if limit:
            query = query.limit(limit)

        if session is None:
            async with new_session() as session:
                return tuple((await session.execute(query)).scalars().all())
        return tuple((await session.execute(query)).scalars().all())

    async def get(
        self,
        _filter: str,
        session: AsyncSession | None = None
    ) -> T | None:
        objs = await self.__get_object_from_db(_filter=_filter, session=session)
        if len(objs) > 1:
            create_log(f'{self.__class__.__name__} > get > got multiple, return 0', 'warning')
        elif len(objs) == 0:
            return None
        return objs[0]

    async def some(
        self,
        _filter: str,
        limit: int | None = None,
        session: AsyncSession | None = None
    ) -> tuple[T, ...]:
        return await self.__get_object_from_db(_filter=_filter, limit=limit, session=session)

    @staticmethod
    async def __add(model: T, session: AsyncSession, commit) -> bool:
        try:
            session.add(model)
            if commit:
                await session.commit()
            return True
        except IntegrityError as e:
            create_log(e, 'error')
            return False

    async def add(
        self,
        model: T,
        session: AsyncSession | None = None,
        commit: bool = False
    ) -> bool:
        if session is None:
            async with new_session() as session:
                return await self.__add(model, session, commit)
        return await self.__add(model, session, commit)

    async def update(self, obj: Type[T], session: AsyncSession | None) -> None:
        pass

    @staticmethod
    async def delete(obj: T, session: AsyncSession | None, commit: bool = False) -> bool:
        try:
            if session is None:
                async with new_session() as session:
                    await session.delete(obj)
                    if commit:
                        await session.commit()
                    return True
            await session.delete(obj)
            if commit:
                await session.commit()
            return True
        except Exception as e:
            create_log(e, 'error')
            return False

    async def all(self, limit: int | None = None, session: AsyncSession | None = None) -> tuple[T, ...]:
        if session is None:
            async with new_session() as session:
                return await self.__get_object_from_db(limit=limit, session=session)
        return await self.__get_object_from_db(limit=limit, session=session)
