import random
import string


def generate_dispatcher_code(length: int = 50) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))