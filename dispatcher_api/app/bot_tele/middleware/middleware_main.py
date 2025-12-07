import logging

from .middleware_abstract import BotMiddleware


class BotMiddlewareMain:
    middlewares: tuple[BotMiddleware, ...]
    def __init__(self, middlewares: tuple[BotMiddleware, ...] = ()) -> None:
        self.middlewares = middlewares

    async def check(self, update: dict) -> tuple[True, str | None] | tuple[False, str]:
        for middleware in self.middlewares:
            ans = await middleware.check(update)
            if not ans[0]:
                logging.warning(f'Middleware {type(middleware).__name__} NOT ALLOWED')
                return ans
        return True, None
