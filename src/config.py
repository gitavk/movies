from pathlib import Path

from pydantic import PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    PROJECT_NAME: str
    API_KEY: str
    API_URL: str = "http://www.omdbapi.com/"
    API_URL_ID: str = API_URL + "?i={imd_id}&pot=full&apikey={API_KEY}"
    API_URL_TITLE: str = API_URL + "?t={title}&pot=full&apikey={API_KEY}"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    SQLALCHEMY_DATABASE_URI: str | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, _v: str | None, values: ValidationInfo) -> str:
        conn_dsn = PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            path=values.data.get("POSTGRES_DB"),
        )
        return str(conn_dsn)


IDS_SOURCE = Path("ids.txt")
RAW_PATH = Path("omdbapi.txt")

settings = Settings()
