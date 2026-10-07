"""Conexao com PostgreSQL.

Melhora o antigo `postgres_connection.py`:

- NAO engole erros silenciosamente (o antigo retornava `[]` em erro de SELECT
  e so dava `print` em erro de modificacao); aqui os erros sao logados e propagados;
- `engine` compartilhado por URI (cache) para reaproveitar o pool de conexoes
  do SQLAlchemy em vez de recria-lo a cada instancia;
- helpers parametrizados por padrao (`fetch_all`, `fetch_one`, `execute`,
  `write_dataframe`) para evitar SQL injection via f-string.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import Row
from sqlalchemy.exc import SQLAlchemyError

from prometheus.config.settings import Environment, Settings, get_settings

logger = logging.getLogger(__name__)

# Cache de engines por URI: o pool do SQLAlchemy e reaproveitado entre conexoes.
_ENGINE_CACHE: dict[str, Engine] = {}


def _get_engine(uri: str, **engine_kwargs: Any) -> Engine:
    if uri not in _ENGINE_CACHE:
        _ENGINE_CACHE[uri] = create_engine(uri, pool_pre_ping=True, **engine_kwargs)
    return _ENGINE_CACHE[uri]


class PostgresConnection:
    """Context manager para acesso a um banco PostgreSQL via SQLAlchemy.

    Uso (leitura):
        with PostgresConnection(environment='prod') as pg:
            linhas = pg.fetch_all(
                'SELECT * FROM processo WHERE criado_em >= :dt',
                {'dt': '2026-01-01'},
            )

    Uso (escrita):
        with PostgresConnection(environment='prod') as pg:
            pg.execute(
                'UPDATE processo SET ativo = true WHERE id = :id',
                {'id': 10},
            )
    """

    def __init__(
        self,
        environment: Environment | str | None = None,
        *,
        uri: str | None = None,
        settings: Settings | None = None,
        **engine_kwargs: Any,
    ) -> None:
        self._settings = settings or get_settings()
        self._uri = uri or self._settings.postgres_uri(environment)
        self.engine = _get_engine(self._uri, **engine_kwargs)
        self._connection = None

    # Ciclo de vida -----------------------------------------------------------
    def __enter__(self) -> PostgresConnection:
        self._connection = self.engine.connect()
        logger.info('Conexao PostgreSQL aberta.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._connection is not None:
            self._connection.close()
            logger.info('Conexao PostgreSQL fechada.')

    # Leitura -----------------------------------------------------------------
    def fetch_all(self, query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Executa um SELECT e retorna lista de dicionarios. Propaga erros."""
        try:
            result = self._conn().execute(text(query), params or {})
            return [dict(row) for row in result.mappings().all()]
        except SQLAlchemyError:
            logger.exception('Erro ao executar consulta.')
            raise

    def fetch_one(self, query: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
        try:
            row: Row | None = self._conn().execute(text(query), params or {}).mappings().first()
            return dict(row) if row is not None else None
        except SQLAlchemyError:
            logger.exception('Erro ao executar consulta (fetch_one).')
            raise

    # Escrita -----------------------------------------------------------------
    def execute(self, query: str, params: dict[str, Any] | list[dict[str, Any]] | None = None) -> int:
        """Executa INSERT/UPDATE/DELETE em transacao. Retorna linhas afetadas.

        Aceita `params` como dict (uma execucao) ou lista de dicts (executemany).
        """
        try:
            with self.engine.begin() as conn:
                result = conn.execute(text(query), params or {})
                return result.rowcount
        except SQLAlchemyError:
            logger.exception('Erro ao executar comando de modificacao.')
            raise

    def write_dataframe(
        self,
        df: pd.DataFrame,
        table: str,
        *,
        schema: str | None = None,
        if_exists: str = 'append',
        index: bool = False,
        chunksize: int = 1000,
    ) -> int:
        """Grava um DataFrame numa tabela usando `to_sql`. Retorna linhas gravadas."""
        if df.empty:
            logger.warning('DataFrame vazio; nada foi gravado em %s.', table)
            return 0
        schema = schema or self._settings.postgres_load_schema
        try:
            with self.engine.begin() as conn:
                df.to_sql(
                    table,
                    conn,
                    schema=schema,
                    if_exists=if_exists,
                    index=index,
                    chunksize=chunksize,
                    method='multi',
                )
            logger.info('Gravadas %d linhas em %s.%s (if_exists=%s).', len(df), schema, table, if_exists)
            return len(df)
        except SQLAlchemyError:
            logger.exception('Erro ao gravar DataFrame em %s.%s.', schema, table)
            raise

    def _conn(self):
        if self._connection is None:
            raise RuntimeError('Conexao nao iniciada. Use dentro de um bloco `with`.')
        return self._connection
