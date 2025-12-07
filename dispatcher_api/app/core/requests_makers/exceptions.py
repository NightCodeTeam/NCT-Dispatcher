class RequestMakersExceptions(Exception):
    pass


class RequestMethodNotFoundException(RequestMakersExceptions):
    def __init__(self, method: str):
        super().__init__(f'Request method not found: {method}')
