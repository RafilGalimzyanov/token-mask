from pydantic import BaseModel, BaseSettings


class DatabaseSettings(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str


class DefaultAdmin(BaseSettings):
    token: str


class Settings(BaseSettings):
    db: DatabaseSettings
    admin: DefaultAdmin

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "_"


settings = Settings()
