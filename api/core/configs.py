from typing import Optional

from pydantic import BaseModel, PostgresDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True


class DatabaseConfig(BaseModel):
    url: str = None
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    port: int = 5432


class JWTConfig(BaseModel):
    secret_key: str = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 31


class LoginConfig(BaseModel):
    level: str = "INFO"
    file_path: Optional[str] = None


class EmailConfig(BaseModel):
    from_email: Optional[str] = None
    from_name: Optional[str] = "TiTruba"
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = 587
    smtp_user: Optional[str] = None
    smtp_name: Optional[str] = None
    smtp_tls: bool = True

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.template"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    jwt: JWTConfig = JWTConfig()
    login: LoginConfig = LoginConfig()
    email: EmailConfig = EmailConfig()

    def get_database_url(self, async_driver: bool = True) -> str:
        """Генерує URL для підключення до бази даних."""

        driver = "postgresql+asyncpg" if async_driver else "postgresql"
        return (f"{driver}://{self.db.user}:{self.db.password}" f"@{self.db.host}:{self.db.port}/{self.db.name}")


settings = Settings()


# def get_settings() -> Settings:
#     """Отримати екземпляр налаштувань (singleton pattern)."""
#     global _settings
#     if _settings is None:
#         _settings = Settings()
#     return _settings
