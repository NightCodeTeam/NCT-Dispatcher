from core.debug import create_log
from core.code_gen import generate_dispatcher_code

from database.session import new_session
from database.repo import DB

from .bot_requests import HttpTeleBot
from .bot_dataclasses.updates_dataclasses import UpdateCallback, UpdateMessage
from .bot_additional_classes import BotStartMessage, BotNewAppMessage, BotError

from .bot_settings import BotCommands, BOT_PREFIX
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

class TeleBotCommands(BaseBotCommands):
    def __init__(self, client: HttpTeleBot):
        super().__init__(client = client)

    @staticmethod
    async def not_found(update: UpdateMessage):
        create_log(f'command_not_found > {update}', 'info')

    @BaseBotCommands.admin_chat
    async def start(self, update: UpdateMessage | UpdateCallback):
        create_log(f'command_start > {update}', 'debug')
        incidents = len(await DB.incidents.only_open())
        if type(update) is UpdateCallback:
            if update.callback_query.message is not None \
            and update.callback_query.message.message_id is not None:
                await self.client.sent_msg(BotStartMessage(
                    incidents, message_id=update.callback_query.message.message_id
                ))
        elif type(update) is UpdateMessage:
            if update.message is not None and update.message.message_id is not None:
                await self.client.sent_msg(BotStartMessage(
                    incidents, message_id=update.message.message_id
                ))

    @BaseBotCommands.admin_chat
    async def new_app(self, update: UpdateMessage):
        create_log(f'command_new_app > {update}', 'debug')
        try:
            app_name, app_url = update.message.text.split('\n')
            app_name = app_name.replace(f'{BOT_PREFIX}{BotCommands.NEW_APP} ', '')

            async with new_session() as session:
                # ? Генерируем код доступа
                dispatcher_codes = [app.dispatcher_code for app in await DB.apps.all(session=session)]
                code = generate_dispatcher_code()
                while True:
                    if code not in dispatcher_codes:
                        break
                    else:
                        code = generate_dispatcher_code()
                await DB.apps.add_app(
                    name=app_name,
                    url='',
                    dispatcher_code=code,
                    session=session,
                    commit=True
                )
                await self.client.sent_msg(
                    BotNewAppMessage(name=app_name, url=app_url, code=code)
                )
        except ValueError:
            create_log(f'Cant unpack app name, url: {update.message.text}')
            await self.client.sent_msg(
                BotError(
                    'Не удалось распаковать name и url приложения'
                )
            )
