try:
    import src
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from contextlib import asynccontextmanager

import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from src.core.debug import logger
from src.core.redis_client import RedisClient
from src.routers import incidents_router_v1, apps_router_v1, auth_router_v1
from src.database import init_db
from src.services import auth_service, blocklist_service

from src.settings import settings


redis_c = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    app.state.redis = RedisClient(
        redis_pool=redis_c,
        prefix=settings.REDIS_PREFIX,
        expire=settings.REDIS_EXPIRE
    )
    yield

if settings.DEBUG:
    app = FastAPI(
        title='NCT Dispatcher',
        version='0.3.0',
        lifespan=lifespan,
    )
else:
    app = FastAPI(
        title='NCT Dispatcher',
        version='0.3.0',
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )

    @app.middleware('http')
    async def blocker(request: Request, call_next):
        if request.client is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        host = request.client.host
        # Проверяем в бане ли пользователь
        if await blocklist_service.in_ban(host, RedisClient(
            redis_pool=redis_c,
            prefix=settings.REDIS_PREFIX,
            expire=settings.REDIS_EXPIRE
        )):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
            )
        # Проверяем не ведет ли эндпойнт в никуда
        exceptions_routes = [ # список эндпоинтов, которые сразу получают бан
            '/.env',
        ]
        if not settings.DEBUG:
            exceptions_routes.extend([
                '/openapi.json',
                '/docs',
                '/redoc',
                '/swagger',
            ])
        routes = tuple([i.path.split('{')[0] for i in app.routes if i not in exceptions_routes])
        if not request.url.path.startswith(routes):
            await blocklist_service.ban(
                ip=host,
                reason='Dispatcher > Endpoint not found',
                duration_days=3,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
            )
        response = await call_next(request)
        return response


app.include_router(incidents_router_v1)
app.include_router(apps_router_v1)
app.include_router(auth_router_v1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_URL.split(','),
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE'],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
