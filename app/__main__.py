import uvicorn
import asyncio
from fastapi import FastAPI

from middleware import AuthAppMiddleware, UnbannedRequestMiddleware
from routers.v1.endpoints import incidents
from database.database import init_db

from settings import settings


app = FastAPI()
app.include_router(incidents.router)

if not settings.DEBUG:
    app.add_middleware(UnbannedRequestMiddleware)
    app.add_middleware(AuthAppMiddleware)


if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run(app, host=settings.FAST_API_HOST, port=settings.FAST_API_PORT)
