from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:///dispatcher.sqlite"

    INCIDENTS_API_PATH: str = "/incidents"
    INCUDENTS_TAGS: list[str] = ["incidents",]

    # env
    TELEGRAM_BOT_TOKEN: str
    FAST_API_HOST: str
    FAST_API_PORT: int
    DEBUG: bool

    class Config:
        env_file = ".env"


settings = Settings()