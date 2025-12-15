import logging
from .bot_dataclasses import UpdateCallback
from .bot_requests import HttpTeleBot



class TeleBotCallbacks:
    def __init__(self, client: HttpTeleBot):
        self.client = client
