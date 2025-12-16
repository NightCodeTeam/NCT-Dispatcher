from .requests_makers import HttpMakerAsync
from settings import settings


class NCTAuth(HttpMakerAsync):
    def __init__(self):
        super().__init__(
            settings.NCT_AUTH_URL,
        )

    async def in_ban(self, user_ip: str) -> bool:
        res = await self._make(f'/v1/bans/{user_ip}', 'GET')
        if res is None:
            return True
        return res.json.get('ok', True)

    async def ban(self, user_ip: str, reason: str | None = None) -> bool:
        res = await self._make(f'/v1/bans/{user_ip}', 'POST', params={'reason': reason})
        if res is None:
            return True
        return res.json.get('ok', False)

    async def bans(self) -> list | tuple:
        res = await self._make('/v1/bans', 'GET')
        if res is None:
            return tuple()
        return res.json.get('bans', tuple())


nct_auth = NCTAuth()
