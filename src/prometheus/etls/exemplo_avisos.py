"""ETL de exemplo: avisos de distribuicao.

Reimplementa, na nova arquitetura, o antigo `etl_aviso_distribuicao.py`:
extrai avisos do MongoDB (origem), achata os documentos e grava num schema
de analytics no PostgreSQL (destino).

Serve de modelo para novas ETLs. Note:
- SELECT/escrita parametrizados (sem f-string em SQL);
- cursor preguicoso no Mongo (sem carregar tudo em memoria de uma vez);
- `write_dataframe` para a carga, com schema vindo da configuracao.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from prometheus.connections.mongo import MongoConnection
from prometheus.connections.postgres import PostgresConnection
from prometheus.core.base_etl import BaseETL

# Data de corte usada no filtro de extracao (exemplo).
DATA_CORTE = datetime(2026, 6, 8, tzinfo=timezone.utc)


class AvisosDistribuicaoETL(BaseETL):
    name = 'avisos_distribuicao'

    def extract(self) -> list[dict[str, Any]]:
        """Extrai avisos da colecao `aviso` no MongoDB da origem."""
        projection = {
            '_id': 0,
            'numero': 1,
            'sistema_webservice': 1,
            'cadastrado_em': 1,
            'distribuido': 1,
            'distribuido_em': 1,
            'processo.orgaoJulgador.nomeOrgao': 1,
            'processo.orgaoJulgador.codigoOrgao': 1,
        }
        filtro = {'cadastrado_em': {'$gte': DATA_CORTE}}

        with MongoConnection(environment=self.environment) as mongo:
            documentos = list(mongo.find('aviso', filtro, projection))

        self.logger.info('Extraidos %d avisos do MongoDB.', len(documentos))
        return documentos

    def transform(self, data: list[dict[str, Any]]) -> pd.DataFrame:
        """Achata os documentos aninhados num formato tabular."""
        linhas = [
            {
                'numero': doc.get('numero'),
                'sistema_webservice': doc.get('sistema_webservice'),
                'cadastrado_em': doc.get('cadastrado_em'),
                'distribuido': doc.get('distribuido'),
                'distribuido_em': doc.get('distribuido_em'),
                'orgao_julgador': doc.get('processo', {}).get('orgaoJulgador', {}).get('nomeOrgao'),
                'codigo_orgao': doc.get('processo', {}).get('orgaoJulgador', {}).get('codigoOrgao'),
            }
            for doc in data
        ]
        return pd.DataFrame(linhas)

    def load(self, data: pd.DataFrame) -> int:
        """Grava os avisos no PostgreSQL de destino."""
        tabela = f'avisos_distribuicao_{self.environment.value}'
        with PostgresConnection(environment=self.environment) as pg:
            return pg.write_dataframe(data, table=tabela, if_exists='replace')


if __name__ == '__main__':
    for ambiente in ('prod', 'hml'):
        AvisosDistribuicaoETL(environment=ambiente).run()
