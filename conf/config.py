from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSchema(BaseModel):
    user: str
    password: str
    database: str
    host: str
    port: int
    debug: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30

    @property
    def url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=f"{self.database}",
            )
        )


class MinioSchema(BaseModel):
    login: str
    password: str
    port: str
    docs_bucket: str
    container_endpoint: str
    outside_endpoint: str


class Settings(BaseSettings):
    postgres: PostgresSchema
    minio: MinioSchema

    model_config = SettingsConfigDict(
        env_file="conf/.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
