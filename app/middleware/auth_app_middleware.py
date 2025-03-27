from typing_extensions import Callable
from fastapi import Request, Response
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from starlette.middleware.base import BaseHTTPMiddleware

from core.debug import create_log
from database.session import new_session
from database.models.app import App
from database.models.banned_ip import BannedIP


class AuthAppMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            async with new_session() as session:
                if request.headers.get('dispatch') is not None \
                and (await request.json()).get('app_name') is not None:
                    app = (await session.execute(
                        select(App).where(and_(
                            App.name == (await request.json())['app_name'],
                            App.dispatcher_code == request.headers.get('dispatch')
                        ))
                    )).scalar_one_or_none()
                    if app is not None:
                        return await call_next(request)
                    session.add(
                        BannedIP(ip = request.client.host, reason="Uncorrected dispatch app code")
                    )
                    await session.commit()
                else:
                    session.add(
                        BannedIP(ip = request.client.host, reason="Not dispatch app code")
                    )
                    #create_log(request.client.host, 'info')
                    await session.commit()
                return Response(status_code=404)
        except IntegrityError:
            create_log(
                f'Auth app error: Add new banned IP but already banned{request.client.host}',
                'info'
            )
            return Response(status_code=404)