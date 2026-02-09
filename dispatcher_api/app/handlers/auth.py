from time import time
from dataclasses import dataclass
from typing import Literal
from pydantic import BaseModel

from fastapi import Request, Response, HTTPException, status

from app.services import auth_service, blocklist_service
from app.core.simplejwt import SimpleJWT, TokenData

from app.settings import settings


class UserLogin(BaseModel):
    name: str
    password: str


class UserRegister(BaseModel):
    name: str
    password: str
    key: str


@dataclass(frozen=True, slots=True)
class User:
    id: int
    name: str


token_types = Literal['access', 'refresh']


class AuthHandler:
    jwt = SimpleJWT(secret_key=settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM)
    """Промежуточный класс авторизации между fastapi и auth_service"""
    @staticmethod
    async def __valid_token_data(token: TokenData, token_key: token_types, host: str):
        """
        Базовая проверка токена
        """
        try:
            assert token.headers['alg'] == settings.AUTH_ALGORITHM
            assert token.headers['typ'] == 'SJWT'
            assert type(token.payload['uid']) is str
            assert type(token.payload['usp']) is int
            assert type(token.payload['exp']) is int
            assert type(token.payload['iat']) is int
            if token_key == 'refresh':
                assert type(token.payload['uni']) is str
                assert len(token.payload['uni']) == 6
            return True
        except (KeyError, AssertionError) as e:
            await blocklist_service.ban(ip=host, reason=f'Dispatcher > Attempt to replace {token_key}')
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token"
            )

    @staticmethod
    def __set_tokens(response: Response, access_token: str, refresh_token: str):
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=not settings.DEBUG,
            secure=not settings.DEBUG,
            samesite='lax',
            max_age=settings.AUTH_ACCESS_EXPIRE
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=not settings.DEBUG,
            secure=not settings.DEBUG,
            samesite='lax',
            max_age=settings.AUTH_REFRESH_EXPIRE_DAYS * 24 * 60 * 60
        )

    async def __create_new_tokens(self, response: Response, refresh_token: str):
        new_tokens = await auth_service.refresh(refresh_token)
        self.__set_tokens(response, new_tokens.access_token, new_tokens.refresh_token)


    async def verify_token(self, request: Request, response: Response) -> User:
        """Попытка проверить токены пользователя."""
        access_token_str = request.cookies.get("access_token")
        access_token = None
        if access_token_str is not None:
            access_token = self.jwt.verify_token(access_token_str)
        if access_token is None:
            # Если токен доступа нет пытаемся найти токен обновления и обновить токен доступа
            refresh_token_str = request.cookies.get("refresh_token")
            if refresh_token_str is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            refresh_token = self.jwt.verify_token(refresh_token_str)
            if refresh_token is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token"
                )
            await self.__valid_token_data(refresh_token, 'refresh', request.client.host)
            await self.__create_new_tokens(
                response=response,
                refresh_token=refresh_token_str
            )
            return User(
                id=refresh_token.payload['uid'],
                name=refresh_token.payload['usp'],
            )
        await self.__valid_token_data(access_token, 'access', request.client.host)
        return User(
            id=access_token.payload['usp'],
            name=access_token.payload['uid'],
        )

    async def login(self, user: UserLogin, response: Response) -> bool:
        tokens = await auth_service.login(name=user.name, password=user.password)
        self.__set_tokens(response, tokens.access_token, tokens.refresh_token)
        return True

    async def register(self, request: Request, user: UserRegister) -> bool:
        if user.key != settings.APP_ACCESS_KEY:
            await blocklist_service.ban(
                ip=request.client.host,
                reason='Dispatcher > Try to parse key'
            )
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail='Goodbuy!'
            )
        return await auth_service.register(
            name=user.name,
            password=user.password,
            key=user.key
        )

    async def logout(self, user: User, response: Response) -> bool:
        ans = await auth_service.logout(user.name)
        if ans:
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
        return ans
