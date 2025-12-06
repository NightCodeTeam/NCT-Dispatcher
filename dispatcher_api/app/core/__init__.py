from os.path import exists
from os import mkdir


from .debug import create_log, init_loggers, call_log, LoggerConfig, RotatingHandlerConfig, StreamHandlerConfig, HandlerConfig
from .dot_env import update_env, env_bool


# Подгружаем в окружение данные из .env
update_env()

if not exists('logs'):
    mkdir('logs')

# Инициализируем необходимые логеры
init_loggers(
    LoggerConfig(
        name='logger',
        level='debug' if env_bool('DEBUG') else 'info',
        handlers=(
            RotatingHandlerConfig(
                maxBytes=1_000,
                backupCount=1,
                filename='logs/logger.log'
            ),
            StreamHandlerConfig()
        )
    ),
    LoggerConfig(
        name='error',
        level='error',
        handlers=(
            HandlerConfig(
                filename='logs/errors.log'
            ),
        )
    )
)


__all__ = (
    'create_log',
    'init_loggers',
    'call_log',
    'LoggerConfig',
    'RotatingHandlerConfig',
    'StreamHandlerConfig'
)
