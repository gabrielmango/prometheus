"""Carregamento e validacao de configuracao.

Substitui o antigo `env_config.py`. Em vez de indexar `config['CHAVE']` no momento
do import (que gera `KeyError` cru quando falta uma variavel), usamos
`pydantic-settings` para:

- carregar o `.env` automaticamente;
- validar tipos e obrigatoriedade com mensagens de erro claras;
- resolver a URI correta por ambiente (dev/tst/hml/preprod/prod) via metodo;
- cachear a instancia com `get_settings()` para nao reler o `.env` a cada chamada.
"""

from __future__ import annotations

from enum import Enum
from functools import lru_cache

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Ambientes suportados pelo template."""

    DEV = 'dev'
    TST = 'tst'
    HML = 'hml'
    PREPROD = 'preprod'
    PROD = 'prod'

    def __str__(self) -> str:  # pragma: no cover - conveniencia de log
        return self.value


class Settings(BaseSettings):
    """Configuracao central da aplicacao, lida do ambiente/.env."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='',
        extra='ignore',
        case_sensitive=False,
    )

    # Ambiente ativo por padrao quando nenhum e passado explicitamente.
    environment: Environment = Field(default=Environment.DEV, alias='PROMETHEUS_ENV')
    log_level: str = Field(default='INFO', alias='LOG_LEVEL')

    # MongoDB -----------------------------------------------------------------
    mongo_uri_dev: str | None = Field(default=None, alias='MONGO_URI_DEV')
    mongo_uri_tst: str | None = Field(default=None, alias='MONGO_URI_TST')
    mongo_uri_hml: str | None = Field(default=None, alias='MONGO_URI_HML')
    mongo_uri_preprod: str | None = Field(default=None, alias='MONGO_URI_PREPROD')
    mongo_uri_prod: str | None = Field(default=None, alias='MONGO_URI_PROD')
    mongo_db_name: str = Field(default='app_db', alias='MONGO_DB_NAME')

    # PostgreSQL --------------------------------------------------------------
    postgres_uri_dev: str | None = Field(default=None, alias='POSTGRES_URI_DEV')
    postgres_uri_tst: str | None = Field(default=None, alias='POSTGRES_URI_TST')
    postgres_uri_hml: str | None = Field(default=None, alias='POSTGRES_URI_HML')
    postgres_uri_preprod: str | None = Field(default=None, alias='POSTGRES_URI_PREPROD')
    postgres_uri_prod: str | None = Field(default=None, alias='POSTGRES_URI_PROD')
    postgres_load_schema: str = Field(default='analytics', alias='POSTGRES_LOAD_SCHEMA')

    # Resolucao por ambiente ---------------------------------------------------
    def mongo_uri(self, environment: Environment | str | None = None) -> str:
        """Retorna a URI do MongoDB para o ambiente informado.

        Levanta `ValueError` com mensagem clara se a URI nao estiver configurada.
        """
        env = self._coerce_env(environment)
        uri = getattr(self, f'mongo_uri_{env.value}')
        if not uri:
            raise ValueError(
                f'URI do MongoDB nao configurada para o ambiente "{env.value}". '
                f'Defina MONGO_URI_{env.value.upper()} no seu .env.'
            )
        return uri

    def postgres_uri(self, environment: Environment | str | None = None) -> str:
        """Retorna a URI do PostgreSQL para o ambiente informado."""
        env = self._coerce_env(environment)
        uri = getattr(self, f'postgres_uri_{env.value}')
        if not uri:
            raise ValueError(
                f'URI do PostgreSQL nao configurada para o ambiente "{env.value}". '
                f'Defina POSTGRES_URI_{env.value.upper()} no seu .env.'
            )
        return uri

    def _coerce_env(self, environment: Environment | str | None) -> Environment:
        if environment is None:
            return self.environment
        if isinstance(environment, Environment):
            return environment
        try:
            return Environment(str(environment).lower())
        except ValueError as exc:
            validos = ', '.join(e.value for e in Environment)
            raise ValueError(f'Ambiente invalido: "{environment}". Use um de: {validos}.') from exc


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retorna a instancia unica de `Settings` (cacheada).

    Converte erros de validacao do pydantic em uma mensagem amigavel.
    """
    try:
        return Settings()
    except ValidationError as exc:  # pragma: no cover - caminho de erro
        raise RuntimeError(f'Configuracao invalida. Verifique seu .env:\n{exc}') from exc
