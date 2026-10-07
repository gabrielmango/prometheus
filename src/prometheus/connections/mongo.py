"""Conexao com MongoDB.

Melhora o antigo `mongodb_magener.py`:

- um unico `MongoConnection` que e um context manager de verdade
  (abre o `MongoClient` na entrada, fecha na saida);
- resolve a URI por ambiente a partir de `Settings`;
- expoe helpers tipados (`find`, `find_one`, `aggregate`, `count`, `collection`)
  sem engolir erros silenciosamente - erros do pymongo sao logados e propagados.
"""

from __future__ import annotations

import logging
from typing import Any, Iterator

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError

from prometheus.config.settings import Environment, Settings, get_settings

logger = logging.getLogger(__name__)


class MongoConnection:
    """Context manager para acesso a um banco MongoDB.

    Uso:
        with MongoConnection(environment='prod') as mongo:
            for doc in mongo.find('aviso', {'ativo': True}, {'_id': 0, 'numero': 1}):
                ...
    """

    def __init__(
        self,
        environment: Environment | str | None = None,
        db_name: str | None = None,
        *,
        uri: str | None = None,
        settings: Settings | None = None,
        **client_kwargs: Any,
    ) -> None:
        self._settings = settings or get_settings()
        self._uri = uri or self._settings.mongo_uri(environment)
        self._db_name = db_name or self._settings.mongo_db_name
        self._client_kwargs = client_kwargs
        self.client: MongoClient | None = None
        self.db: Database | None = None

    # Ciclo de vida -----------------------------------------------------------
    def __enter__(self) -> MongoConnection:
        try:
            self.client = MongoClient(self._uri, **self._client_kwargs)
            self.db = self.client[self._db_name]
            logger.info('Conexao MongoDB aberta (db=%s).', self._db_name)
            return self
        except PyMongoError:
            logger.exception('Falha ao conectar ao MongoDB (db=%s).', self._db_name)
            if self.client is not None:
                self.client.close()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.client is not None:
            self.client.close()
            logger.info('Conexao MongoDB fechada (db=%s).', self._db_name)

    # Acesso ------------------------------------------------------------------
    def collection(self, name: str) -> Collection:
        if self.db is None:
            raise RuntimeError('Conexao nao iniciada. Use dentro de um bloco `with`.')
        return self.db[name]

    def find(
        self,
        collection: str,
        filtro: dict[str, Any] | None = None,
        projection: dict[str, Any] | None = None,
        *,
        limit: int = 0,
        batch_size: int = 1000,
    ) -> Iterator[dict[str, Any]]:
        """Itera documentos de forma preguicosa (cursor), economizando memoria."""
        try:
            cursor = self.collection(collection).find(filtro or {}, projection, batch_size=batch_size)
            if limit > 0:
                cursor = cursor.limit(limit)
            yield from cursor
        except PyMongoError:
            logger.exception('Erro ao buscar documentos na colecao %s.', collection)
            raise

    def find_one(
        self,
        collection: str,
        filtro: dict[str, Any] | None = None,
        projection: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        try:
            return self.collection(collection).find_one(filtro or {}, projection)
        except PyMongoError:
            logger.exception('Erro ao buscar documento na colecao %s.', collection)
            raise

    def aggregate(self, collection: str, pipeline: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
        try:
            yield from self.collection(collection).aggregate(pipeline)
        except PyMongoError:
            logger.exception('Erro no aggregate da colecao %s.', collection)
            raise

    def count(self, collection: str, filtro: dict[str, Any] | None = None) -> int:
        try:
            return self.collection(collection).count_documents(filtro or {})
        except PyMongoError:
            logger.exception('Erro ao contar documentos na colecao %s.', collection)
            raise
