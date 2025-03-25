from core.debug import create_log
from .bot_dataclasses import UpdateCallback
from .bot_requests import HttpTeleBot

#from text_messages import


class TeleBotCallbacks:
    def __init__(self, client: HttpTeleBot):
        self.client = client
