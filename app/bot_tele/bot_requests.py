import json

from sqlalchemy.engine import create

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
        #AdminChatMiddleware(),
        #UserBannedMiddleware(),
        #ChatBannedMiddleware()
    ))
    last_update = 0 # необходимо для работы по api

    def __init__(self):
        super().__init__(
            base_url='https://api.telegram.org'
        )

    @staticmethod
    def __get_update_data(update_dict: dict) -> Update | None:
        return get_update_dc(update_dict)

    def _set_middlewares(self, middlewares: tuple[BotMiddleware, ...]):
        self.middleware.middlewares = middlewares

    async def get_updates(self) -> tuple[Update, ...]:
        res = await self._make(
            url=f'/bot{self.token}/getUpdates',
            method='GET',
            params={
                'offset': self.last_update,
                'limit': BOT_MAX_UPDATES
            }
        )
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
                        await self.sent_msg2(
                            chat_id=env_int("TELEGRAM_ADMIN_CHAT"),
                            message=msg
                        )
                    self.last_update = update['update_id'] + 1
                return tuple(ans)
            create_log(f'Bot cant get updates: > res is not OK: {res.json}', 'error')
        create_log('Bot cant get updates: > res is None', 'error')
        return ()

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


    async def sent_msg2(self, chat_id: int, message: str, data: dict | None = None, addition_params: dict | None = None) -> bool:
        params = {
            'chat_id': chat_id,
            'text': message
        }
        if addition_params is not None:
            params.update(addition_params)
        res = await self._make(
                    url=f'/bot{self.token}/sendMessage',
                    method='GET',
                    params=params,
                    data=data,
                )
        if res is not None:
            return True if res.json['ok'] else False
        create_log('Bot cant send msg: > res is None', 'error')
        return False

    async def sent_msg_reply(self, chat_id: int, message_id: int, message: str, data: dict | None = None):
        return await self.sent_msg(
            chat_id=chat_id,
            message=message,
            data=data,
            addition_params={
                'reply_to_message_id': message_id,
                #'reply_parameters': {
                #    'message_id': message_id,
                #},
            }
        )

    async def edit_message_text2(self, chat_id: int, message_id: int, new_message: str, addition_data: dict | None = None):
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': new_message,
        }
        if addition_data is not None:
            data.update(addition_data)
        res = await self._make(
                    url=f'/bot{self.token}/editMessageText',
                    method='GET',
                    data=data,
                )
        if res is not None:
            return True if res.json['ok'] else False
        create_log('Bot cant edit msg text: > res is None', 'error')
        return False

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


    async def edit_message_reply_markup2(self, chat_id: int, message_id: int, new_reply_markup: dict, addition_data: dict | None = None):
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reply_markup': new_reply_markup,
        }
        if addition_data is not None:
            data.update(addition_data)
        res = await self._make(
                    url=f'/bot{self.token}/editMessageReplyMarkup',
                    method='GET',
                    data=data,
                )
        if res is not None:
            return True if res.json['ok'] else False
        create_log('Bot cant edit msg text: > res is None', 'error')
        return False

    async def get_chat(self, chat_id: int) -> dict | None:
        return (await self._make(url=f'/bot{self.token}/getChat', method='GET', params={'chat_id': chat_id})).json
