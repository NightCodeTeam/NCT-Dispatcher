import uvicorn
import asyncio
from threading import Thread
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.debug import logger
from routers import incidents_router_v1, apps_router_v1, auth_router_v1
from database import init_db

from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


if settings.DEBUG:
    app = FastAPI(
        title='NCT Dispatcher',
        version='0.2.0',
        lifespan=lifespan,
    )
else:
    app = FastAPI(
        title='NCT Dispatcher',
        version='0.2.0',
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )
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
