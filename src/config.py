from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    debug: bool
    db_user: str
    db_host: str
    db_port: int
    db_name: str
    db_pass: str
    model_config = SettingsConfigDict(env_file='.env')
    echo: bool = True
    driver: str = "postgresql+asyncpg"

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}"

settings = Settings()
