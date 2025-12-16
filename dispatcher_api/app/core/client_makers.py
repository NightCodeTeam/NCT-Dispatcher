from .requests_makers import HttpMakerAsync
from settings import settings


class NCTAuth(HttpMakerAsync):
    def __init__(self):
        super().__init__(
            settings.NCT_AUTH_URL,
        )

    async def in_ban(self, user_ip: str) -> bool:
        return (await self._make(f'/v1/bans/{user_ip}', 'GET')).json.get('ok', True)

    async def ban(self, user_ip: str, reason: str | None = None) -> bool:
        return await self._make(f'/v1/bans/{user_ip}', 'POST', params={'reason': reason}).json.get('ok', False)

    async def bans(self) -> list | tuple:
        return (await self._make('/v1/bans', 'GET')).json.get('bans', [])


nct_auth = NCTAuth()
