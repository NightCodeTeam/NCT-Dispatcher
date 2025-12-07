import re
import logging

from .bot_settings import BotCallbacks


def parse_bot_callback_id(callback_string: str) -> int | None:
    try:
        ans = re.search(r'[0-9]+', callback_string)
        if ans is None:
            return None
        return int(ans.group(0))
    except ValueError:
        logging.error(f"Invalid callback: {callback_string}")
        return None


def parse_bot_callback_command(callback_string: str) -> str:
    try:
        ans = re.search(r'[a-zA-Z_]+', callback_string)
        if ans is None:
            return ''
        return ans.group(0)
    except ValueError:
        logging.error(f"Invalid callback: {callback_string}")
        return ''
