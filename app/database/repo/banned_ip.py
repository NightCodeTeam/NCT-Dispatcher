from typing import override

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core import create_log
from database.models.banned_ip import BannedIP
from .base_repo import Repository


class BannedIPRepo(Repository):
    def __init__(self):
        super().__init__(BannedIP)

    @override
    async def get(
            self,
            _filter: str,
            session: AsyncSession | None = None
    ) -> BannedIP | None:
        return await super().get(_filter=_filter, session=session)

    @override
    async def some(
            self,
            _filter: str,
            limit: int | None = None,
            session: AsyncSession | None = None
    ) -> tuple[BannedIP, ...] | None:
        return await super().some(_filter=_filter, session=session)

    @override
    async def add(self, obj: BannedIP, session: AsyncSession | None = None, commit: bool = False) -> bool:
        return await super().add(model=obj, session=session, commit=False)

    # async def update(self, obj: Type[T], session: AsyncSession | None) -> None:
    #    pass

    @override
    async def delete(self, obj: BannedIP, session: AsyncSession | None = None, commit: bool = False) -> bool:
        return await super().delete(obj=obj, session=session)

    @override
    async def all(self, limit: int | None = None, session: AsyncSession | None = None) -> tuple[BannedIP, ...]:
        return await super().all(limit=limit, session=session)

    async def get_ip_by_ip(self, ip_address: str, session: AsyncSession) -> BannedIP | None:
        return await self.get(_filter=f"{self.table_name}.ip='{ip_address}'", session=session)

    async def add_ban(self, ip_address: str, reason: str, session: AsyncSession, commit: bool = False) -> bool:
        try:
            return await self.add(BannedIP(
                ip=ip_address,
                reason=reason
            ), session=session, commit=commit)
        except IntegrityError:
            create_log(f'Cant insert {ip_address}: its exists', 'error')
            return False

    async def delete_by_ip(self, ip_address: str, session: AsyncSession, commit: bool = False) -> bool:
        data = await self.get_ip_by_ip(ip_address, session)
        if data:
            return await self.delete(data, session, commit)
        return False
