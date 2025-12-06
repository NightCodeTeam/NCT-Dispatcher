import asyncio

from core.debug import create_log
from .bot_dataclasses import Update, UpdateMessage, UpdateCallback
from .bot_requests import HttpTeleBot
from .bot_callback_class import TeleBotCallbacks
from .bot_commands_class import TeleBotCommands
from .bot_parser import parse_bot_callback_command

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
                case BotCommands.NEW_APP:
                    await self.commands.new_app(update)

                case _:
                    await self.commands.not_found(update)

    async def parse_callback(self, update: UpdateCallback):
        if update.callback_query.data is not None:
            match parse_bot_callback_command(update.callback_query.data):
                case BotCallbacks.BACK:
                    #await self.commands.start(update)
                    await self.callbacks.back(update)
                case BotCallbacks.ALL_INCIDENTS:
                    await self.callbacks.all_incidents(update)
                case BotCallbacks.OPEN_INCIDENTS:
                    await self.callbacks.open_incidents(update)
                case BotCallbacks.SELECT_INCIDENT:
                    await self.callbacks.select_incident(update)
                case BotCallbacks.CLOSE_INCIDENT:
                    await self.callbacks.close_incident(update)
                case BotCallbacks.DEL_INCIDENT:
                    await self.callbacks.del_incident(update)
                case BotCallbacks.ALL_APPS:
                    await self.callbacks.all_apps(update)
                case BotCallbacks.SELECT_APP_INCIDENTS:
                    await self.callbacks.app_selected_incidents(update)
                #case BotCallbacks.NEW_APP:
                #    await self.callbacks.new_app(update)
                case BotCallbacks.NEW_APP_CONFIRM:
                    await self.callbacks.new_app_confirm(update)
                case BotCallbacks.NEW_APP_CANCEL:
                    await self.callbacks.new_app_cancel(update)
                case BotCallbacks.SELECT_APP:
                    await self.callbacks.select_app(update)
                case BotCallbacks.DEL_APP:
                    await self.callbacks.del_app(update)
                case BotCallbacks.ALL_BANS:
                    await self.callbacks.bans(update)
                case BotCallbacks.SELECT_BAN:
                    await self.callbacks.select_ban(update)
                case BotCallbacks.DELETE_BAN:
                    await self.callbacks.del_ban(update)
                case _:
                    create_log(f'Unknown callback command: {update.callback_query.data}', 'error')
