import logging
import requests

from .dispatcher_settings import Level


class Dispatcher:
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

    def send(
        self,
        title: str,
        message: str,
        level: Level,
        logs: str | list[str] | tuple[str] | None = None,
        max_logs_to_send: int = 10,
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
        res = requests.post(
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
        return True if res is not None and res.json()['ok'] == True else False

    def get_logs_from_file(self, log_file_path: str) -> tuple[str, ...]:
        with open(log_file_path, 'r') as f:
            return tuple(f.readlines())

    def get_last_logs(self) -> tuple[str]:
        # ? Определяем логеры
        if self.__loggers is None or len(self.__loggers) == 0:
            loggers = [logging.getLogger(),]
        else:
            loggers = self.loggers_names_to_loggers_classes(self.__loggers)

        # ? Находим файлы логгеров
        files = []
        for logger in loggers:
            for handler in logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    files.append(handler.baseFilename)

        # ?
        last_logs = []
        for f in files:
            last_logs.extend(self.get_logs_from_file(f)[-self.__max_logs_to_send:])
        return tuple(last_logs)

    @staticmethod
    def loggers_names_to_loggers_classes(loggers_names: list[str]) -> list[logging.Logger]:
        return [logging.getLogger(logger_name) for logger_name in loggers_names]

    @staticmethod
    def logs_list_to_str(logs: tuple[str]) -> str:
        return '\n'.join(logs)
