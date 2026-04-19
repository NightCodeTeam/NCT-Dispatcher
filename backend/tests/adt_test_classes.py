class RedisClientMock:
    def __init__(self, *args, **kwargs):
        pass

    async def delete(self, *args, **kwargs):
        return True

    async def set_json(self, *args, **kwargs):
        return True

    async def get_json(self, *args, **kwargs):
        return {}
