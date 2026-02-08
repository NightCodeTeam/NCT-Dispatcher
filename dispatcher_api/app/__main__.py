try:
    import app
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from contextlib import asynccontextmanager

import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.core.debug import logger
from app.core.redis_client import RedisClient
from app.routers import incidents_router_v1, apps_router_v1, auth_router_v1
from app.database import init_db
from app.services import auth_service, blocklist_service

from app.settings import settings


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
        # Проверяем в бане ли пользователь
        if await blocklist_service.in_ban(request.client.host, RedisClient(
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
                ip=request.client.host,
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
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    logger.log('Init fastapi', 'info')
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
