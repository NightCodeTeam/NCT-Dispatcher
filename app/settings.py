from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:///dispatcher.sqlite3"

    # env
    BOT_SLEEP: int | float
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_CHAT: int
    FAST_API_HOST: str
    FAST_API_PORT: int
    DEBUG: bool

    class ConfigDict:
        env_file = ".env"

settings = Settings()