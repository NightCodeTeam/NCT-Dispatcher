from datetime import datetime
from dataclasses import dataclass

from fastapi import HTTPException

from app.core.requests_makers import HttpMakerAsync
from app.core.redis_client import RedisClient

from app.settings import settings


@dataclass(frozen=True, slots=True)
class AuthToken:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True)
class User:
    id: int
    name: str
    is_admin: str
    is_active: str
    last_active: datetime
    key_id: int


class AuthService(HttpMakerAsync):
    def __init__(self):
        super().__init__(
            base_url=settings.AUTH_URL,
            base_headers={
                'X-Access-Code': settings.AUTH_ACCESS_CODE,
                'X-App-Name': settings.AUTH_APP_NAME
            }
        )

    @staticmethod
    async def __cache(redis: RedisClient, key: str) -> dict | None:
        return await redis.get_dict(
            key=key,
            spec_app_prefix=settings.BLOCKER_REDIS_PREFIX
        )

    async def login(self, name: str, password: str) -> AuthToken:
        ans = await self._make('/v1/auth/login', method='POST', json={'name': name, 'password': password})
        if ans.status != 200:
            raise HTTPException(
                status_code=ans.status,
                detail=ans.json.get('detail', 'Unknown error')
            )
        return AuthToken(ans.json['access_token'], ans.json['refresh_token'])

    async def logout(self, name: str) -> bool:
        ans = await self._make('/v1/auth/logout', method='POST', json={'name': name})
        if ans.status != 200:
            raise HTTPException(
                status_code=ans.status,
                detail=ans.json.get('detail', 'Unknown error')
            )
        return ans.json['ok']

    async def refresh(self, refresh_token: str) -> AuthToken:
        ans = await self._make('/v1/auth/refresh', method='POST', json={'refresh_token': refresh_token})
        if ans.status != 200:
            raise HTTPException(
                status_code=ans.status,
                detail=ans.json.get('detail', 'Unknown error')
            )
        return AuthToken(ans.json['access_token'], ans.json['refresh_token'])

    async def register(self, name: str, password: str, key: str) -> bool:
        return (await self._make('/v1/auth/register', method='POST', json={
            'name': name,
            'password': password,
            'key': key
        })).json['ok']

    async def user_by_id(self, user_id: int, redis: RedisClient) -> User:
        data = await self.__cache(redis, f'get_user:user_id:{user_id}')
        if data is not None:
            return data
        ans = await self._make(f'/v1/auth/users/{user_id}')
        if ans.status != 200:
            raise HTTPException(
                status_code=ans.status,
                detail=ans.json.get('detail', 'Unknown error')
            )
        return User(**ans.json)


auth_service = AuthService()
