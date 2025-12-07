from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    # env
    DEBUG: bool
    HOST: str
    PORT: int
    DB_PATH: str
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_CHAT: int
    BOT_SLEEP: int
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    AUTH_TOKEN_LIFETIME_IN_MIN: int
    FRONTEND_URL: str
    NCT_AUTH_URL: str


settings = Settings()
