from typing_extensions import Callable
from fastapi import Request, Response
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware

from database.utils import get_banned_ips_from_db
from database.models.banned_ip import BannedIP


class UnbannedRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if request.client is not None:
            banned = await get_banned_ips_from_db(f'bannedips.ip == "{request.client.host}"')
            if len(banned) > 0:
                return Response(status_code=404)
        return Response(status_code=404)
