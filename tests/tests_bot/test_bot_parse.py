from app.bot_tele.bot_parser import parse_bot_callback_id, parse_bot_callback_command
from app.bot_tele.bot_settings import BotCallbacks


def test_parse_bot_callback_id():
    assert parse_bot_callback_id('test_1') == 1
    assert parse_bot_callback_id('_1123') == 1123
    assert parse_bot_callback_id('1') == 1
    assert parse_bot_callback_id('0') == 0
    assert parse_bot_callback_id('') == None
    assert parse_bot_callback_id('test') == None
    assert parse_bot_callback_id('test 1') == 1


def test_parse_bot_callback_command():
    assert parse_bot_callback_command('test_1') == 'test_'
    assert parse_bot_callback_command('_1123') == '_'
    assert parse_bot_callback_command('') == ''

    commands = [{'command': command, 'value': value} for command, value in vars(BotCallbacks).items() if not command.startswith('__')]
    for command in commands:
        assert parse_bot_callback_command(f'{command['value']}123') == command['value']

