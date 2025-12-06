from abc import ABC
from typing import TypeVar, Type, Optional, AsyncGenerator
from sqlalchemy import text, select, delete, exists, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.debug import logger
from app.core.single import Singleton
from ..database import Base
from ..session import new_session


T = TypeVar('T', bound=Base)


class Repository(ABC, Singleton):
    table_name: str

    def __init__(self, model: Type[T], relationships: Optional[list[str, ...] | tuple[str, ...]] = None):
        self.model = model
        self.table_name = model.__tablename__
        self.relationships = relationships

    async def __get_object_from_db(
        self,
        _filter: str | None = None,
        limit: int | None = None,
        session: AsyncSession | None = None,
        load_relations: bool = True,
    ) -> tuple[T]:
        query = select(self.model)
        if load_relations and self.relationships:
            for relationship in self.relationships:
                if hasattr(self.model, relationship):
                    query = query.options(selectinload(getattr(self.model, relationship)))

        if _filter is not None:
            query = query.filter(text(_filter))
        if limit:
            query = query.limit(limit)

        if session is None:
            async with new_session() as session:
                return tuple((await session.execute(query)).scalars().all())
        return tuple((await session.execute(query)).scalars().all())

    async def get(
        self,
        _filter: str,
        session: AsyncSession | None = None,
        load_relations: bool = True,
    ) -> T | None:
        objs = await self.__get_object_from_db(_filter=_filter, session=session, load_relations=load_relations)
        if len(objs) > 1:
            logger.log(f'{self.__class__.__name__} > get > got multiple, return 0', 'warning')
        elif len(objs) == 0:
            return None
        return objs[0]

    async def some(
        self,
        _filter: str,
        limit: int | None = None,
        session: AsyncSession | None = None,
        load_relations: bool = True,
    ) -> tuple[T, ...]:
        return await self.__get_object_from_db(_filter=_filter, limit=limit, session=session, load_relations=load_relations)

    @staticmethod
    async def __add(model: T, session: AsyncSession, commit: bool = False) -> bool:
        try:
            session.add(model)
            if commit:
                await session.commit()
            return True
        except IntegrityError as e:
            logger.log(e, 'error')
            return False

    async def add(
        self,
        model: T,
        session: AsyncSession | None = None,
        commit: bool = False,
    ) -> bool:
        if session is None:
            async with new_session() as session:
                return await self.__add(model, session, commit)
        return await self.__add(model, session, commit)

    @staticmethod
    async def add_many(self,
        objs: tuple[Type[T]] | list[Type[T]],
        session: AsyncSession | None = None,
        commit: bool = False
    ) -> None:
        if session is None:
            async with new_session() as session:
                session.add_all(objs)
        else:
            session.add_all(objs)
        if commit:
            await session.commit()

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
            logger.log(e, 'error')
            return False

    async def all(
        self,
        limit: int | None = None,
        session: AsyncSession | None = None,
        load_relations: bool = True,
    ) -> tuple[T, ...]:
        if session is None:
            async with new_session() as session:
                return await self.__get_object_from_db(limit=limit, session=session, load_relations=load_relations)
        return await self.__get_object_from_db(limit=limit, session=session, load_relations=load_relations)

    async def clear_table(self, session: AsyncSession | None = None, commit: bool = False) -> bool:
        if session is None:
            async with new_session() as ss:
                await ss.execute(delete(self.model))
                if commit:
                    await ss.commit()
                return True
        await session.execute(delete(self.model))
        if commit:
            await session.commit()
        return True

    async def _exists(self, _filter: str, session: AsyncSession) -> bool:
        return bool(await session.scalar(select(exists().select_from(self.model).where(text(_filter)))))

    async def count(self, session: AsyncSession | None = None) -> int:
        if session:
            return (await session.execute(select(func.count()).select_from(self.model))).scalar()
        async with new_session() as n_session:
            return (await n_session.execute(select(func.count()).select_from(self.model))).scalar()

    async def all_gen(self, session: AsyncSession | None = None, load_relations: bool = False, skip: int = 0, search_field: str = 'id') -> AsyncGenerator[Type[T]]:
        for i in range(skip, await self.count(session=session)):
            yield await self.get(f'{self.model.__tablename__}.{search_field}={i}', load_relations=load_relations, session=session)

    async def pagination(
        self,
        skip: int | None = None,
        limit: int | None = None,
        session: AsyncSession | None = None,
        load_relations: bool = False,
        search_field: str = 'id'
    ) -> tuple[T, ...]:
        _filter = ''
        if skip:
            _filter += f'{self.model.__tablename__}.{search_field}>={skip}'
        if skip and limit:
            _filter += ' AND '
        if limit:
            _filter += f'{self.model.__tablename__}.{search_field}<{skip + limit}'
        return await self.some(
            _filter=_filter,
            session=session,
            load_relations=load_relations,
        )
