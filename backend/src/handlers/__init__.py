from src.settings import settings

from .auth import UserLogin, UserRegister, User

if settings.DEBUG:
    from .auth import AuthHandlerBase as AuthHandler
else:
    from .auth import AuthHandler

from .apps import AppHandler
