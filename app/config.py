"""
Project configuration classes
"""

from functools import lru_cache
from typing import Type, Tuple

from sqlalchemy.engine import URL

from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    PydanticBaseSettingsSource
)


class BaseSettingsYAML(BaseSettings):
    """This class customizes source to read the YAML file"""

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Customizing settings source"""
        return (YamlConfigSettingsSource(settings_cls),)


class LabConfigurations(BaseSettingsYAML):
    """Labs common configurations class"""
    model_config = SettingsConfigDict(yaml_file="lab_configurations.yaml", yaml_file_encoding="utf-8")

    neowise_api_url: str


class AppConfiguration(BaseSettings):
    """App configuration class"""
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    TOKEN: str


class PostgresConfiguration(BaseSettings):
    """Postgres configuration class"""
    model_config = SettingsConfigDict(env_file='postgres.env', env_file_encoding='utf-8')

    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    ASYNC_POSTGRES_URL: str | URL = ""

    @field_validator("ASYNC_POSTGRES_URL", mode="after")
    def build_async_db_url(cls, v: str | None, info: FieldValidationInfo) -> str | URL:
        """
        Builds database connection URL after model validation,
        if it was not provided within .env file
        """
        if not v:
            return URL.create(
                drivername="postgresql+asyncpg",
                username=info.data["POSTGRES_USER"],
                password=info.data["POSTGRES_PASSWORD"],
                host=info.data["POSTGRES_HOST"],
                port=info.data["POSTGRES_PORT"],
                database=info.data["POSTGRES_DB"],
                query={},
            )
        return v


@lru_cache
def get_postgres_conf() -> PostgresConfiguration:
    """Provides PostgresConfiguration instance"""
    return PostgresConfiguration()  # type: ignore


@lru_cache
def get_app_conf() -> AppConfiguration:
    """Provides AppConfiguration instance"""
    return AppConfiguration()  # type: ignore


@lru_cache
def get_lab_conf() -> LabConfigurations:
    """Provides LabConfigurations instance"""
    return LabConfigurations()  # type: ignore
