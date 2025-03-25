import asyncio
from core.debug import create_log
from .bot_dataclasses import Update, UpdateMessage, UpdateCallback
from .bot_requests import HttpTeleBot
from .bot_callback_class import TeleBotCallbacks
from .bot_commands_class import TeleBotCommands

from .bot_settings import BOT_PREFIX, BOT_SLEEP_TIME_IN_SEC, BotCommands, BotCallbacks


class TeleBot:
    def __init__(self):
        self.listens = []

        self.client = HttpTeleBot()
        self.commands = TeleBotCommands(self.client)
        self.callbacks = TeleBotCallbacks(self.client)

    async def run(self):
        # Запускаем главный цикл
        try:
            while True:
                await self.get_updates()
                # Асинхронно отдыхаем
                await asyncio.sleep(BOT_SLEEP_TIME_IN_SEC)
        except asyncio.exceptions.CancelledError as e:
            create_log(f'Stopping TeleBot > {e}', 'info')

    async def get_updates(self):
        # ! Главный метод отвечает за получение обновлений
        for update in await self.client.get_updates():
            await self.parse_update(update)

    async def parse_update(self, update: Update):
        if type(update) is UpdateMessage:
            await self.parse_command(update)
        elif type(update) is UpdateCallback:
            await self.parse_callback(update)

    async def parse_command(self, update: UpdateMessage):
        # Метод парсит команды и определяет какую команду запустить
        if update.message.text is not None and update.message.text.startswith(BOT_PREFIX):
            match update.message.text.split(' ')[0][1:].lower():
                case BotCommands.START | BotCommands.HELP:
                    await self.commands.start(update)

                case _:
                    await self.commands.not_found(update)

    async def parse_callback(self, update: UpdateCallback):
        if update.callback_query.data is not None:
            pass