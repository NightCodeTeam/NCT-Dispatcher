from core.requests_makers import HttpMakerAsync
from core.redis_client import RedisClient

from app.settings import settings


class BlocklistService(HttpMakerAsync):
    def __init__(self):
        super().__init__(
            base_url=settings.BLOCKER_URL,
            base_headers={
                'X-Access-Code': settings.BLOCKER_ACCESS_CODE
            }
        )

    async def in_ban(self, ip: str, redis: RedisClient) -> bool:
        data = await redis.get_json(
            key=f'in_ban:ip_address:{ip}',
            spec_app_prefix=settings.BLOCKER_REDIS_PREFIX
        )
        if data is not None and type(data.get('ok')) == bool:
            return data['ok']
        return (await self._make(f'/v1/bans/{ip}', method='GET')).json.get('ok', False)

    async def ban(
        self, ip: str,
        reason: str = 'no reason',
        duration_days: int = 3,
        permanent: bool = False,
        white: bool = False
    ) -> bool:
        return (await self._make(f'/v1/bans', method='POST', json={
            'ip': ip,
            'reason': reason,
            'duration_days': duration_days,
            'permanent': permanent,
            'white': white
        })).json.get('ok', False)


blocklist_service = BlocklistService()
