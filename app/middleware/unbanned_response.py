from typing_extensions import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from core.debug import create_log
from core.replacers import rm_http
from database.utils import get_banned_ips_from_db


class UnbannedRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if request.client is not None:
            banned = await get_banned_ips_from_db(f'bannedips.ip == "{rm_http(request.client.host)}"')
            if len(banned) > 0:
                create_log(f'Banned ip request > {rm_http(request.client.host)}', 'info')
                return Response(status_code=404)
        create_log(f'Request client is None > {request}', 'warning')
        return Response(status_code=404)
