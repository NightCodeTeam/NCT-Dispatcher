from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from .base import Repository


class UserRepo(Repository):
    def __init__(self):
        super().__init__(User, ('apps', 'edited_incidents'))

    async def exists(self, username: str, session: AsyncSession) -> bool:
        return await self._exists(f"{self.table_name}.name='{username}'", session=session)

    async def by_name(
        self,
        username: str,
        session: AsyncSession,
        load_relations: bool = False
    ) -> User | None:
        return await super().get(
            f"{self.table_name}.name='{username}'",
            session=session,
            load_relations=load_relations
        )

    async def by_id(
        self,
        user_id: int,
        session: AsyncSession,
        load_relations: bool = False
    ) -> User | None:
        return await self.get(
            f"{self.table_name}.id={user_id}",
            session=session,
            load_relations=load_relations
        )

    async def new(
        self,
        username: str,
        password: str,
        session: AsyncSession,
        commit: bool = True
    ) -> bool:
        return await self.add(User(
            name=username,
            password=password,
        ), session=session, commit=commit)
