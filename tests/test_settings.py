"""Testes da configuracao e da abstracao BaseETL (sem bancos reais)."""

from __future__ import annotations

import pytest

from prometheus.config.settings import Environment, Settings
from prometheus.core.base_etl import BaseETL


def _settings() -> Settings:
    # _env_file=None evita ler um .env real durante os testes.
    return Settings(
        _env_file=None,
        PROMETHEUS_ENV='dev',
        MONGO_URI_DEV='mongodb://localhost:27017',
        POSTGRES_URI_PROD='postgresql+psycopg2://u:p@localhost:5432/db',
    )


def test_resolve_uri_por_ambiente():
    s = _settings()
    assert s.mongo_uri('dev') == 'mongodb://localhost:27017'
    assert s.postgres_uri(Environment.PROD).endswith('/db')


def test_uri_ausente_gera_erro_claro():
    s = _settings()
    with pytest.raises(ValueError, match='MONGO_URI_PROD'):
        s.mongo_uri('prod')


def test_ambiente_invalido():
    s = _settings()
    with pytest.raises(ValueError, match='Ambiente invalido'):
        s.mongo_uri('producao')


def test_base_etl_orquestra_etapas():
    s = _settings()
    chamadas: list[str] = []

    class FakeETL(BaseETL):
        name = 'fake'

        def extract(self):
            chamadas.append('extract')
            return [1, 2, 3]

        def transform(self, data):
            chamadas.append('transform')
            return [x * 2 for x in data]

        def load(self, data):
            chamadas.append('load')
            return sum(data)

    resultado = FakeETL(environment='dev', settings=s).run()
    assert resultado == 12
    assert chamadas == ['extract', 'transform', 'load']
