def test_decorator(func):
    def wrapper(*args, **kwargs):
        print('ssss')
        result = func(*args, **kwargs)

        return result
    return wrapper


def test_function():
    print('test')
