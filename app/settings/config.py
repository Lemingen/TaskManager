from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_EXIT_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_ENTER_PORT: int
    DB_HOST: str
    DB_NAME_SERVICE: str

    model_config = SettingsConfigDict(env_file= '.env', env_file_encoding= 'utf-8')

    @property
    def get_async_db_url(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_NAME_SERVICE}:{self.DB_ENTER_PORT}/{self.DB_NAME}'

    @property
    def get_sync_db_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_NAME_SERVICE}:{self.DB_ENTER_PORT}/{self.DB_NAME}"

    @property
    def get_dev_async_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_EXIT_PORT}/{self.DB_NAME}"

    @property
    def get_dev_sync_db_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_EXIT_PORT}/{self.DB_NAME}"

settings = Settings()