import uvicorn
import asyncio
from threading import Thread
from fastapi import FastAPI

from bot_tele.bot_main import TeleBot
from routers.v1 import incident_router
from database.database import init_db

from settings import settings


app = FastAPI(title='NCT Dispatcher', docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(incident_router.router)

#if not settings.DEBUG:
#    app.add_middleware(UnbannedRequestMiddleware)
#    app.add_middleware(AuthAppMiddleware)


async def run_bot():
    bot = TeleBot()
    await bot.run()


def generate_bot():
    asyncio.run(run_bot())


if __name__ == "__main__":
    asyncio.run(init_db())

    thread = Thread(target=generate_bot, name='bot')
    thread.daemon = True
    thread.start()

    uvicorn.run(app, host=settings.FAST_API_HOST, port=settings.FAST_API_PORT)
