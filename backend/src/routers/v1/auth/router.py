from fastapi import APIRouter, status, Response
from fastapi.requests import Request

from core.pydantic_misc_models import Ok
from core.fast_decorators import cache, rate_limiter
from core.redis_client import RedisDep
from src.handlers import AuthHandler, UserLogin, UserRegister
from src.depends import UserDep
from .models import User


auth_router_v1 = APIRouter(prefix='/v1/auth', tags=['auth'])


@auth_router_v1.post('/login', response_model=Ok)
async def login(response: Response, user_data: UserLogin):
    """
    Вход пользователя в систему.
    """
    return {'ok': await AuthHandler().login(user_data, response)}


@auth_router_v1.post('/refresh', response_model=Ok)
async def refresh(request: Request, response: Response):
    """
    Обновление токена доступа.
    """
    #await auth.refresh(request=request, response=response)
    return {'ok': True}


@auth_router_v1.post('/logout', response_model=Ok)
async def logout(response: Response, user: UserDep):
    """
    Выход пользователя из системы.
    """
    return {'ok': await AuthHandler().logout(user=user, response=response)}


@auth_router_v1.post('/register', response_model=Ok)
async def register(request: Request, user_data: UserRegister):
    """
    Регистрация нового пользователя.
    """
    return {'ok': await AuthHandler().register(request=request, user=user_data)}


@auth_router_v1.get('/who_am_i', response_model=User)
@rate_limiter(10, 30)
async def who_am_i(request: Request, response: Response, user: UserDep):
    """
    Возвращает информацию о текущем пользователе.
    """
    return {'name': user.name}
