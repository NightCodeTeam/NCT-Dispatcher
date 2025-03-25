from .middleware_abstract import BotMiddleware
from settings import settings


class AdminChatMiddleware(BotMiddleware):
    async def check(self, update: dict) -> tuple[True, str | None] | tuple[False, str]:
        if update['message']['chat']['id'] == settings.TELEGRAM_ADMIN_CHAT:
            return True, None
        return False, 'Not admin chat'