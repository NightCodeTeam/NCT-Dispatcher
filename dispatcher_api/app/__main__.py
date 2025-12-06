import uvicorn
import asyncio
from threading import Thread

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.bot_tele.bot_main import TeleBot
from app.routers import incidents_router_v1
from app.database import init_db

from settings import settings


if settings.DEBUG:
    app = FastAPI(
        title='NCT Dispatcher',
        version='0.2.0',
    )
else:
    app = FastAPI(
        title='NCT Dispatcher',
        version='0.2.0',
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )
app.include_router(incidents_router_v1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE'],
    allow_headers=["*"],
)

async def run_bot():
    bot = TeleBot()
    await bot.run()


def generate_bot():
    asyncio.run(run_bot())


if __name__ == "__main__":
    asyncio.run(init_db())

    thread = Thread(target=generate_bot, name='nct_dispatcher_bot')
    thread.daemon = True
    thread.start()

    uvicorn.run(app, host=settings.FAST_API_HOST, port=settings.FAST_API_PORT)
