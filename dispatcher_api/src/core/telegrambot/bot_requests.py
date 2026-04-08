import logging

from .bot_dataclasses import Update, BotMessage
from .bot_dataclasses.utility import get_update_dc
from .middleware.middleware_abstract import BotMiddleware
from core.requests_makers import HttpMakerAsync


class HttpTeleBot(HttpMakerAsync):
    __last_update = 0 # необходимо для работы updates
    def __init__(
        self,
        token: str,
        middlewares: tuple | None = None,
        max_updates_per_sync: int = 100,
        tries_to_reconnect: int = 3,
        timeout_in_sec: int = 10,
    ):
        super().__init__(
            base_url=f'https://api.telegram.org/bot/{token}',
            tries_to_reconnect=tries_to_reconnect,
            timeout_in_sec=timeout_in_sec,
        )
        self.max_updates_per_sync = max_updates_per_sync
        if middlewares is None:
            middlewares = tuple()
        self.__middlewares = middlewares

    @staticmethod
    def __text_transfer(text: str) -> str:
        for i in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '\\', '-', '=', '|', '{', '}', '.', '!'):
            text = text.replace(i, f'\\{i}')
        return text

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
                text=self.__text_transfer(message.text),
                reply_to_message_id=message.reply_to_message_id,
                reply_markup=message.reply_markup,
            )

            # Отправляем
            return func(self, *args, **kwargs, message=message)
        return wrapper

    @staticmethod
    def __get_update_data(update_dict: dict) -> Update | None:
        return get_update_dc(update_dict)

    def _set_middlewares(self, middlewares: tuple[BotMiddleware, ...]):
        self.__middlewares.middlewares = middlewares

    async def get_updates(self) -> tuple[Update, ...]:
        logging.log(10, f'{self.__class__.__name__} > get updates from {self.__last_update}')
        res = await self._make(
            url=f'/getUpdates',
            method='GET',
            params={
                'offset': self.__last_update,
                'limit': self.max_updates_per_sync
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
                                logging.error(e)
                        self.__last_update = update['update_id'] + 1
                    return tuple(ans)
                logging.warning(f'{self.__class__.__name__} > res is not OK: {res.json}')
            logging.warning(f'{self.__class__.__name__} > res is None')
            return ()
        except KeyError as e:
            logging.critical(e)
            return ()

    @protect_text
    async def sent_msg(self, message: BotMessage, adt_data: dict | None = None) -> bool:
        data = message.to_dict
        if adt_data is not None:
            data.update(adt_data)
        res = await self._make(
                url=f'/sendMessage',
                method='GET',
                data=data,
            )
        if res is not None:
            return res.json.get('ok', False)
        logging.error(f'{self.__class__.__name__} > cant send message: > res is not OK: {res}')
        return False

    @protect_text
    async def edit_message_text(self, message: BotMessage):
        res = await self._make(
            url=f'/editMessageText',
            method='GET',
            data=message.to_dict,
        )

        if res is not None and res.json['ok']:
            return True
        logging.error(f'Bot cant edit msg text: > {res}')
        return False

    @protect_text
    async def edit_message_reply_markup(self, message: BotMessage):
        res = await self._make(
            url=f'/editMessageReplyMarkup',
            method='GET',
            data=message.to_dict,
        )

        if res is not None and res.json['ok']:
            return True
        logging.error(f'{self.__class__.__name__} > cant edit msg reply markup: > {res}')
        return False
