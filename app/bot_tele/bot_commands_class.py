from core.debug import create_log
from database.session import new_session
from database.utils import get_incidents_from_db

from .bot_requests import HttpTeleBot
from .bot_dataclasses.updates_dataclasses import UpdateMessage
from .bot_additional_classes import BotStartMessage

from .bot_settings import BotCommands, BOT_PREFIX
from settings import settings
#from text_messages import


class TeleBotCommands:
    def __init__(self, client: HttpTeleBot):
        self.client = client

    async def not_found(self, update: UpdateMessage):
        create_log(f'command_not_found > {update}', 'debug')
        await self.client.sent_msg_reply(
            update.message.chat.id,
            update.message.message_id,
            f'Команда не найдена: {update.message.text.split(' ')[0] if update.message.text is not None else ''}\nИспользуйте команду /start чтобы узнать подробности',
        )

    async def start(self, update: UpdateMessage):
        create_log(f'command_start > {update}', 'debug')
        incedents = len(await get_incidents_from_db('incidents.status = "open"'))
        await self.client.sent_msg(BotStartMessage(incedents, message_id=update.message.message_id))


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
                create_log(f'Update is None in Admin call {func.__name__}', 'error')
                return None

            if update.message.chat.id == settings.TELEGRAM_ADMIN_CHAT:
                return await func(*args, **kwargs)

            if update.message.from_user is not None:
                create_log(
                    f'User {update.message.from_user.first_name} ({update.message.from_user.id}) try use admin command {func.__name__}',
                    'info'
                )
            else:
                create_log(f'Chat {update.message.chat.id} try use admin command {func.__name__}', 'info')
            return None
        return wrapper
