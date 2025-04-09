from .middleware_abstract import BotMiddleware
from settings import settings


class AdminChatMiddleware(BotMiddleware):
    async def check(self, update: dict) -> tuple[bool, str | None]:
        if update.get('message') is not None:
            if update['message']['chat']['id'] == settings.TELEGRAM_ADMIN_CHAT:
                return True, None
        if update.get('callback_query') is not None:
            if update['callback_query']['message']['chat']['id'] == settings.TELEGRAM_ADMIN_CHAT:
                return True, None
        return False, 'Not admin chat'