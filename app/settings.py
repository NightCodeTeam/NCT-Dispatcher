from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:///dispatcher.sqlite3"

    INCIDENTS_API_PATH: str = "/incidents"
    INCIDENTS_TAGS: list[str] = ["incidents",]

    # env
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_CHAT: int
    FAST_API_HOST: str
    FAST_API_PORT: int
    DEBUG: bool

    class Config:
        env_file = ".env"


settings = Settings()