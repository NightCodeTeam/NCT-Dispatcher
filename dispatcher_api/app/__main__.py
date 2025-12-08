import uvicorn
import asyncio
from threading import Thread
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.debug import logger
from bot_tele.bot_main import TeleBot
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

async def run_bot():
    bot = TeleBot()
    await bot.run()


def generate_bot():
    asyncio.run(run_bot())


if __name__ == "__main__":
    logger.log('Init bot', 'info')
    #thread = Thread(target=generate_bot, name='nct_dispatcher_bot')
    #thread.daemon = True
    #thread.start()

    logger.log('Init fastapi', 'info')
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
