from typing_extensions import Callable
from fastapi import Request, Response
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware

from database.session import get_session, new_session
from database.models.banned_ip import BannedIP


class UnbannedRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if request.client is not None:
            async with new_session() as session:
                banned = (await session.execute(
                    select(BannedIP).where(BannedIP.ip == (request.client.host))
                )).scalar_one_or_none()
                if banned is not None:
                    return Response(status_code=404)
            return await call_next(request)
        return Response(status_code=404)
