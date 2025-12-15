from random import randint

from fastapi import APIRouter, HTTPException, status

from settings import settings
from .models import Token, UserLogin
from routers.misc_models import Ok
from depends import SessionDep
from database import DB
from core.auth import verify_hashed, create_access_token, get_hash
from core.trash import generate_trash_string


auth_router_v1 = APIRouter(prefix='/v1/auth', tags=['auth'])


@auth_router_v1.post('/login', response_model=Token)
async def login(user_data: UserLogin, session: SessionDep):
    user = await DB.users.by_name(user_data.username, session)
    if not user or not verify_hashed(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректное имя пользователя или пароль",
        )
    return {
        "access_token": create_access_token(data={
            "sub": user.name,
            generate_trash_string(randint(3, 6)): generate_trash_string(randint(5, 20))
        }),
        "token_type": "Bearer"
    }


@auth_router_v1.post('/register', response_model=Ok)
async def register(user_data: UserLogin, session: SessionDep):
    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    if len(user_data.username) < 6 or len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Логин или пароль должны быть больше 6"
        )

    if await DB.users.exists(user_data.username, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Имя пользователя уже существует"
        )

    if not await DB.users.new(user_data.username, get_hash(user_data.password), session):
        raise HTTPException(status_code=400, detail="Внутренняя ошибка приложения, свяжитесь с администрацией")
    return {'ok': True}
