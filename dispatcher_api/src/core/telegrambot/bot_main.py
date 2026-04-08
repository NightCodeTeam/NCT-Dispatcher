import asyncio
import logging

from .bot_requests import HttpTeleBot
from .bot_callback_class import TeleBotCallbacks
from .bot_commands_class import TeleBotCommands
from .bot_dataclasses import Update, UpdateMessage, UpdateCallback
from .exceptions import NotUnderstandableUpdate


class TeleBot:
    def __init__(
        self,
        token: str,
        commands: dict,
        callbacks: dict,
        middlewares: tuple | None = None,
        sleep_time_in_sec: int = 60,
        max_updates_per_sync: int = 100,
        command_prefix: str = '/',
        tries_to_reconnect: int = 3,
        timeout_in_sec: int = 10,
    ):
        self.listens = []

        self.client = HttpTeleBot(
            token=token,
            middlewares=middlewares,
            max_updates_per_sync=max_updates_per_sync,
            tries_to_reconnect=tries_to_reconnect,
            timeout_in_sec=timeout_in_sec,
        )
        self.commands = TeleBotCommands(self.client)
        self.callbacks = TeleBotCallbacks(self.client)

        self.sleep = sleep_time_in_sec
        self.prefix = command_prefix

    async def run(self):
        # Запускаем главный цикл
        try:
            while True:
                await self.get_updates()
                # Асинхронно отдыхаем
                await asyncio.sleep(self.sleep)
        except asyncio.exceptions.CancelledError as e:
            logging.info(f'Stopping TeleBot > {e}')

    async def get_updates(self):
        # ! Главный метод отвечает за получение обновлений
        for update in await self.client.get_updates():
            await self.parse_update(update)

    async def parse_update(self, update: Update):
        if type(update) is UpdateMessage:
            await self.parse_command(update)
        elif type(update) is UpdateCallback:
            await self.parse_callback(update)
        else:
            raise NotUnderstandableUpdate(update)

    async def parse_command(self, update: UpdateMessage):
        pass

    async def parse_callback(self, update: UpdateCallback):
        pass
