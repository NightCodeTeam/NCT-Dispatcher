from fastapi import APIRouter, status, Response
from fastapi.requests import Request

from app.core.pydantic_misc_models import Ok
from app.core.fast_decorators import cache, rate_limiter
from app.core.redis_client import RedisDep
from app.handlers.auth import AuthHandler, UserLogin, UserRegister
from app.depends import UserDep


auth_router_v1 = APIRouter(prefix='/v1/auth', tags=['auth'])


@auth_router_v1.post('/login', response_model=Ok)
async def login(response: Response, user_data: UserLogin):
    return {'ok': await AuthHandler().login(user_data, response)}


@auth_router_v1.post('/refresh', response_model=Ok)
async def refresh(request: Request, response: Response):
    #await auth.refresh(request=request, response=response)
    return {'ok': True}


@auth_router_v1.post('/logout', response_model=Ok)
async def logout(response: Response, user: UserDep):
    return {'ok': await AuthHandler().logout(user=user, response=response)}


@auth_router_v1.post('/register', response_model=Ok)
async def register(request: Request, user_data: UserRegister):
    return {'ok': await AuthHandler().register(request=request, user=user_data)}


@auth_router_v1.get('/who_am_i', response_model=Ok)
#@cache('auth:who')
@rate_limiter(10, 30)
async def who_am_i(request: Request, response: Response, user: UserDep, redis: RedisDep):
    return {'name': user.name}
