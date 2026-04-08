import logging
from abc import ABC, abstractmethod


class BotMiddleware(ABC):
    @staticmethod
    def __key_check_decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except KeyError as e:
                logging.log(40, f'{func.__name__} key error {e}', 'error')
                return False, 'Exce'
        return wrapper

    @__key_check_decorator
    @abstractmethod
    async def check(self, update: dict) -> tuple[True, str | None] | tuple[False, str]:
        """Главный метод, если возвращает False значит запрос от телеграмма не достигает дальнейшей логики приложения.
        Выход:
        True / False - удовлетворяет ли запрос условиям
        str / None - сообщение, которое уйдет в логгер например "Пользователь не прошел проверку"
        """
        pass
