from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    # env
    DEBUG: bool

    HOST: str
    PORT: int

    DB_PATH: str
    APP_ACCESS_KEY: str

    AUTH_URL: str
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    AUTH_ACCESS_EXPIRE: int
    AUTH_REFRESH_EXPIRE_DAYS: int
    AUTH_REDIS_PREFIX: str
    AUTH_ACCESS_CODE: str
    AUTH_APP_NAME: str

    REDIS_URL: str
    REDIS_EXPIRE: int
    REDIS_POOL_SIZE: int
    REDIS_PREFIX: str

    BLOCKER_URL: str
    BLOCKER_REDIS_PREFIX: str
    BLOCKER_ACCESS_CODE: str

    FRONTEND_URL: str


settings = Settings()
