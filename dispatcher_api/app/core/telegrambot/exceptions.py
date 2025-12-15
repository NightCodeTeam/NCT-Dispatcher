from .bot_dataclasses.updates_dataclasses import Update, UpdateCallback


class SimpleTelegramBotException(Exception):
    def __init__(self, txt: str):
        super().__init__(txt)


class NotUnderstandableUpdate(SimpleTelegramBotException):
    def __init__(self, update: Update):
        super().__init__(f"Update {update} not understandable")


class BotMessageNoneException(SimpleTelegramBotException):
    def __init__(self, update: Update):
        txt = f'Message is None: {update.update_id}'
        super().__init__(txt)


class BotCallbackDataNoneException(SimpleTelegramBotException):
    def __init__(self, update: UpdateCallback):
        txt = f'CallbackData is None: {update.update_id}'
        super().__init__(txt)
