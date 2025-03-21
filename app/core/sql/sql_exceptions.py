from core.debug import create_log


class SQLInjectionException(Exception):
    def __init__(self, injection: str, word: str) -> None:
        msg = f'SQL injection founded: {injection} -> {word}'
        create_log(msg, 'error')
        super().__init__(msg)
