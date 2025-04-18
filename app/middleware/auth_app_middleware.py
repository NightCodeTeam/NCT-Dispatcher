import json

from typing_extensions import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import IntegrityError

from core.debug import create_log
from core.replacers import rm_http
from database.session import new_session
from database.models import App, BannedIP
from database.utils import get_apps_from_db


class AuthAppMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            async with new_session() as session:
                if request.headers.get('dispatch') is not None \
                and (await request.json()).get('app_name') is not None:
                    app_name = (json.loads(await request.body())).get('app_name')
                    code = request.headers.get('dispatch')
                    app = await get_apps_from_db(
                        f'apps.name = "{app_name}"\
                         AND apps.dispatcher_code = "{code}"'
                    )
                    #app = (await session.execute(
                    #    select(App).where(and_(
                    #        App.name == (await request.json())['app_name'],
                    #        App.dispatcher_code == request.headers.get('dispatch')
                    #    ))
                    #)).scalar_one_or_none()
                    if app[0] is not None:
                        create_log(f'App: {app[0].name} got access', 'info')
                        return await call_next(request)
                    create_log(f'Incorrect dispatch app name or code > {app_name}\
                               {request.headers.get('dispatch')}')
                    session.add(
                        BannedIP(ip = rm_http(request.client.host), reason="Uncorrected dispatch app code")
                    )
                    await session.commit()
                else:
                    app_name = (json.loads(await request.body())).get('app_name')
                    create_log(f"New ban > dispatch = {request.headers.get('dispatch')}\n\
                    app = {app_name}", 'info')
                    session.add(
                        BannedIP(ip = rm_http(request.client.host), reason="Not dispatch app code")
                    )
                    await session.commit()
                return Response(status_code=404)
        except IntegrityError:
            create_log(
                f'Auth app error: Add new banned IP but already banned{request.client.host}',
                'info'
            )
            return Response(status_code=404)
        except json.JSONDecodeError as e:
            create_log(
                f'Json error:', 'crit'
            )
            create_log(
                e, 'crit'
            )
            return Response(status_code=404)