from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    debug: bool
    db_user: str
    db_host: str
    db_port: int
    db_name: str
    db_pass: str
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
