from datetime import datetime
from dataclasses import dataclass

from fastapi import HTTPException

from src.core.requests_makers import HttpMakerAsyncImproved
from src.core.redis_client import RedisClient

from src.settings import settings


@dataclass(frozen=True, slots=True)
class AuthToken:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True)
class User:
    id: int
    name: str
    is_admin: bool
    is_active: bool
    last_active: datetime
    key_id: int


class AuthService(HttpMakerAsyncImproved):
    def __init__(self):
        super().__init__(
            base_url=settings.AUTH_URL,
            base_headers={
                'X-Access-Code': settings.AUTH_ACCESS_CODE,
                'X-App-Name': settings.AUTH_APP_NAME
            },
            parse_method=self._get_simple_response,
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
        data = await self.redis_cache(redis, f'get_user:user_id:{user_id}', settings.BLOCKER_REDIS_PREFIX)
        if data is not None:
            return User(**data)
        ans = await self._make(f'/v1/auth/users/{user_id}')
        if ans.status != 200:
            raise HTTPException(
                status_code=ans.status,
                detail=ans.json.get('detail', 'Unknown error')
            )
        return User(**ans.json)


auth_service = AuthService()
