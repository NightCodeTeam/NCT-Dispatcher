from .bot_requests import HttpTeleBot


class TeleBotCallbacks:
    def __init__(self, client: HttpTeleBot):
        self.client = client
