from core.debug import create_log
from core.requests_makers import HttpMakerAsync
from core.dot_env import env_int
from .bot_dataclasses import Update, BotMessage, BotReplyMarkup, BotInlineKeyboardLine
from .bot_dataclasses.utility import get_update_dc
from .middleware.middleware_main import BotMiddlewareMain
from .middleware.middleware_abstract import BotMiddleware
from .middleware.middleware_admin_chat import AdminChatMiddleware

from .bot_settings import BOT_MAX_UPDATES
from settings import settings

class HttpTeleBot(HttpMakerAsync):
    token = settings.TELEGRAM_BOT_TOKEN
    # Middleware - это какая либо защита от атак на бота если её пропустили сервера телеграмм
    middleware = BotMiddlewareMain((
        AdminChatMiddleware(),
        #UserBannedMiddleware(),
        #ChatBannedMiddleware()
    ))
    __last_update = 0 # необходимо для работы по api

    def __init__(self):
        super().__init__(
            base_url='https://api.telegram.org'
        )

    @staticmethod
    def protect_text(func):
        def wrapper(self, *args, **kwargs):
            # Находим сообщение
            message = kwargs.get('message')
            if message is None:
                if len(args) > 0:
                    message = args[0]
            if message is None or type(message) is not BotMessage:
                return func(self, *args, **kwargs)

            # Обновляем его
            message = BotMessage(
                chat_id=message.chat_id,
                message_id=message.message_id,
                text=message.text.replace('.', '\\.'),
                reply_to_message_id=message.reply_to_message_id,
                reply_markup=message.reply_markup,
            )

            # Отправляем
            return func(self, message=message)
        return wrapper

    @staticmethod
    def __get_update_data(update_dict: dict) -> Update | None:
        return get_update_dc(update_dict)

    def _set_middlewares(self, middlewares: tuple[BotMiddleware, ...]):
        self.middleware.middlewares = middlewares

    async def get_updates(self) -> tuple[Update, ...]:
        create_log(f'Bot > get updates {self.__last_update}')
        res = await self._make(
            url=f'/bot{self.token}/getUpdates',
            method='GET',
            params={
                'offset': self.__last_update,
                'limit': BOT_MAX_UPDATES
            }
        )
        try:
            if res is not None:
                if res.json['ok']:
                    ans: list[Update] = []
                    for update in res.json['result']:
                        passing, msg = await self.middleware.check(update)
                        if passing:
                            try:
                                update_dc = self.__get_update_data(update)
                                if update_dc is not None:
                                    ans.append(update_dc)
                            except KeyError as e:
                                create_log(e, 'error')
                        else:
                            await self.sent_msg(BotMessage(
                                chat_id=env_int("TELEGRAM_ADMIN_CHAT"),
                                text=msg if msg is not None else 'Error no message'
                            ))
                        self.__last_update = update['update_id'] + 1
                    return tuple(ans)
                create_log(f'Bot cant get updates: > res is not OK: {res.json}', 'error')
            create_log('Bot cant get updates: > res is None', 'error')
            return ()
        except KeyError as e:
            create_log(e, 'error')
            return ()

    @protect_text
    async def sent_msg(self, message: BotMessage, data: dict | None = None) -> bool:
        res = await self._make(
                url=f'/bot{self.token}/sendMessage',
                method='GET',
                params=message.to_dict,
                data=data,
            )
        if res is not None and res.json['ok']:
            return True
        create_log(f'Bot cant send message: > res is not OK: {res}', 'error')
        return False

    @protect_text
    async def edit_message_text(self, message: BotMessage):
        res = await self._make(
            url=f'/bot{self.token}/editMessageText',
            method='GET',
            data=message.to_dict,
        )

        if res is not None and res.json['ok']:
            return True
        create_log(f'Bot cant edit msg text: > {res}', 'error')
        return False

    @protect_text
    async def edit_message_reply_markup(self, message: BotMessage):
        res = await self._make(
            url=f'/bot{self.token}/editMessageReplyMarkup',
            method='GET',
            data=message.to_dict,
        )

        if res is not None and res.json['ok']:
            return True
        create_log(f'Bot cant edit msg reply markup: > {res}', 'error')
        return False

    async def get_chat(self, chat_id: int) -> dict | None:
        res = await self._make(url=f'/bot{self.token}/getChat', method='GET', params={'chat_id': chat_id})
        return res.json if res is not None else None
