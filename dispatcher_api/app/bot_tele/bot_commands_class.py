import  logging

from .bot_requests import HttpTeleBot
from .bot_dataclasses.updates_dataclasses import UpdateCallback, UpdateMessage

from settings import settings


class BaseBotCommands:
    def __init__(self, client: HttpTeleBot):
        self.client = client

    # ! Проверка что команда админская
    @staticmethod
    def admin_chat(func):
        async def wrapper(*args, **kwargs):
            update: UpdateMessage | None = None
            try:
                if type(args[1]):
                    update = args[1]
            except IndexError:
                update = kwargs.get('update')
            if update is None:
                logging.error(f'Update is None in Admin call {func.__name__}')
                return None

            if update.message.chat.id == settings.TELEGRAM_ADMIN_CHAT:
                return await func(*args, **kwargs)

            if update.message.from_user is not None:
                logging.info(
                    f'User {update.message.from_user.first_name} ({update.message.from_user.id}) try use admin command {func.__name__}',
                )
            else:
                logging.info(f'Chat {update.message.chat.id} try use admin command {func.__name__}')
            return None
        return wrapper


class TeleBotCommands(BaseBotCommands):
    def __init__(self, client: HttpTeleBot):
        super().__init__(client = client)

    @staticmethod
    async def not_found(update: UpdateMessage):
        logging.info(f'command_not_found > {update}')

    @BaseBotCommands.admin_chat
    async def start(self, update: UpdateMessage | UpdateCallback):
        logging.debug(f'command_start > {update}')
        pass