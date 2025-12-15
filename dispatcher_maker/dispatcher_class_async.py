import aiohttp

from .dispatcher_settings import Level


class DispatcherAsync:
    def __init__(
        self,
        dispatcher_url: str,
        app_name: str,
        dispatcher_code: str,
        loggers_paths: list[str] | None = None,
        max_logs_to_send: int = 10,
    ):
        self.__dispatcher_url = dispatcher_url
        self.__code = dispatcher_code
        self.__app_name = app_name
        self.__loggers = loggers_paths
        self.__max_logs_to_send = max_logs_to_send

    async def send(
        self,
        title: str,
        message: str,
        level: Level,
        logs: str | list[str] | tuple[str] | None = None,
    ) -> bool:
        if type(logs) in (list, tuple):
            logs='\n'.join(logs)
        else:
            logs = ''
            try:
                for i in self.__loggers:
                    with open(i, 'r') as f:
                        logs = '\n'.join(f.readlines()[-self.__max_logs_to_send:])
            except FileNotFoundError:
                logs = 'Logs not found'
        async with aiohttp.ClientSession() as session:
            res = await session.post(
                self.__dispatcher_url,
                json={
                    'incident': {
                        'title': title,
                        'message': message,
                        'logs': logs,
                        'level': level,
                    },
                    'app_name': self.__app_name,
                    'code': self.__code,
                }
            )
            return True if res is not None and (await res.json())['ok'] == True else False
