import logging
from .bot_requests import HttpTeleBot
from .bot_dataclasses.updates_dataclasses import UpdateCallback, UpdateMessage


class BaseBotCommands:
    def __init__(self, client: HttpTeleBot):
        self.client = client


class TeleBotCommands(BaseBotCommands):
    def __init__(self, client: HttpTeleBot):
        super().__init__(client = client)
