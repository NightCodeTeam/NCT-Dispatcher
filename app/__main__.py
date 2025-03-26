import uvicorn
import asyncio
from threading import Thread
from fastapi import FastAPI

from bot_tele.bot_main import TeleBot
from middleware import AuthAppMiddleware, UnbannedRequestMiddleware
from routers.v1.endpoints import incidents
from database.database import init_db

from settings import settings


app = FastAPI()
app.include_router(incidents.router)

if not settings.DEBUG:
    app.add_middleware(UnbannedRequestMiddleware)
    app.add_middleware(AuthAppMiddleware)


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
