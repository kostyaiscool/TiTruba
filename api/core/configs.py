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


class JWTSettings(BaseModel):
    secret_key: str = Field(description="Секретный ключ для Джи Вити")
    algorithm: str = Field(default="HS256", description="Это алгоритм")
    access_token_expire_minutes: int = Field(default=15, description="Время жизни бедного токена", ge=1)
    refresh_token_expire_days: int = Field(default=31, description="Время жизни богатого токена", ge=1)


class LoginSettings(BaseModel):
    level: str = Field(default="INFO", description="Уровень логирования")
    file_path: Optional[str] = Field(default=None, description="Путь к пользовательскому сердцу через Польшу, Северную Корую, и Китай")


class EmailSettings(BaseModel):
    from_email: Optional[str] = Field(default=None, description="Почта, из которой мы будем отправлять письма любви")
    from_name: Optional[str] = Field(default="TiTruba", description="Имя отправителя, Саша Крутой 228420")
    smtp_host: Optional[str] = Field(default=None, description="ТыПочта")
    smtp_port: Optional[int] = Field(default=587, description="Портишка братишка")
    smtp_user: Optional[str] = Field(default=None, description="От чего имени будет настройки")
    smtp_name: Optional[str] = Field(default=None, description="Так чье имя?")
    smtp_tls: bool = Field(default=True, description="Защита и шифрования")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.template"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__"
    )
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    jwt: JWTSettings = JWTSettings()
    login: LoginSettings = LoginSettings()
    email = EmailSettings = EmailSettings()

    def get_database_url(self, async_driver: bool = True) -> str:
        """Генерує URL для підключення до бази даних."""

        driver = "postgresql+asyncpg" if async_driver else "postgresql"
        return (f"{driver}://{self.db.user}:{self.db.password}" f"@{self.db.host}:{self.db.port}/{self.db.name}")


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Отримати екземпляр налаштувань (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
