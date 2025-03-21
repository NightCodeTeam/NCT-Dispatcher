from typing_extensions import Callable
from fastapi import Request, Response
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware

from database.session import new_session
from database.models.app import App


class AuthAppMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if request.headers.get('dispatch') is not None:
            async with new_session() as session:
                app = (await session.execute(
                    select(App).filter(App.name == request.headers.get('app'))
                )).first()
                if app is not None and app.dispatch == request.headers.get('dispatch'):
                    return await call_next(request)
        return Response(status_code=400)
