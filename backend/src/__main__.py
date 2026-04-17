try:
    import src
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from contextlib import asynccontextmanager

import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from core.redis_client import RedisClient
from core.fast_middlewares import blocker_check
from src.routers import incidents_router_v1, apps_router_v1, auth_router_v1
from src.database import init_db
from src.services import blocklist_service

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_URL.split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware('http')
async def blocker(request: Request, call_next):
    await blocker_check(
        request=request,
        app=app,
        blocklist_service=blocklist_service,
        settings=settings,
        redis_client=RedisClient(
            redis_pool=redis_c,
            prefix=settings.REDIS_PREFIX,
            expire=settings.REDIS_EXPIRE
        ),
        exceptions_routes=[
            '/.env'
        ],
    )
    return await call_next(request)


app.include_router(incidents_router_v1)
app.include_router(apps_router_v1)
app.include_router(auth_router_v1)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
