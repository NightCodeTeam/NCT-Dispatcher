import uvicorn
import asyncio
from threading import Thread
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from core.debug import logger
from core.client_makers import nct_auth
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

    @app.middleware("http")
    async def catch_all_middleware(request: Request, call_next):
        if nct_auth.in_ban(user_ip=request.client.host):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        response = await call_next(request)
        # Если получен 404, вызываем нашу функцию
        if response.status_code == 404:
            return nct_auth.ban(user_ip=request.client.host, reason='Dispatcher try get unknown route')
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
