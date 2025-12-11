import logging
from random import randint

from fastapi import APIRouter, HTTPException, status

from .models import Token, UserLogin
from routers.misc_models import Ok
from depends import SessionDep
from database import DB
from core.auth import verify_hashed, create_access_token
from core.trash import generate_trash_string


auth_router_v1 = APIRouter(prefix='/v1/auth', tags=['auth'])


@auth_router_v1.post('/login', response_model=Token | Ok)
async def login(user_data: UserLogin, session: SessionDep):
    logging.info(f'login > {user_data.username}')
    user = await DB.users.by_name(user_data.username, session)
    if not user or not verify_hashed(user.password, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректное имя пользователя или пароль",
        )
    return {
        "access_token": create_access_token(data={
            "sub": user.name,
            generate_trash_string(randint(3, 6)): generate_trash_string(randint(5, 20))
        }),
        "token_type": "bearer"
    }


@auth_router_v1.post('/test', response_model=Token | Ok)
async def test(session: SessionDep):

    print('aLll good')
    return {'ok': await DB.incidents.new(
        title='test',
        message='test',
        logs='-',
        level='debug',
        app_id=1,
        session=session,
        commit=True
    )}