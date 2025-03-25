from typing_extensions import Callable
from fastapi import Request, Response
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware

from database.session import new_session
from database.models.app import App
from database.models.banned_ip import BannedIP


class AuthAppMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        async with new_session() as session:
            if request.headers.get('dispatch') is not None:
                app = (await session.execute(
                    select(App).filter(App.name == request.headers.get('app'))
                )).first()
                if app is not None and app.dispatch == request.headers.get('dispatch'):
                    return await call_next(request)
                session.add(
                    BannedIP(ip = request.client.ip, reason="Uncorrected dispatch app code")
                )
                await session.commit()
            else:
                session.add(
                    BannedIP(ip = request.client.ip, reason="Not dispatch app code")
                )
                await session.commit()
            return Response(status_code=400)
