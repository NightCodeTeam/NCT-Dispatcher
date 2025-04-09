from core.debug import create_log
from bot_tele.bot_dataclasses.updates_dataclasses import Update, UpdateCallback


class BotMessageNoneException(Exception):
    def __init__(self, update: Update):
        txt = f'Message is None: {update.update_id}'
        create_log(txt, 'error')
        super().__init__(txt)


class BotCallbackDataNoneException(Exception):
    def __init__(self, update: UpdateCallback):
        txt = f'CallbackData is None: {update.update_id}'
        create_log(txt, 'error')
        super().__init__(txt)
