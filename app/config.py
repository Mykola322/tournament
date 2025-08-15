from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sqlalchemy_uri: str = "mysql+aiomysql://localhost:5432/db_name"
    secret_key: str = "your secret key"
    algorithm: str = "jwt algorithm"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()