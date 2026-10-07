"""Registro de ETLs disponiveis.

Para adicionar uma nova ETL:
    1. crie um modulo em `prometheus/etls/<sua_etl>.py` com uma classe que herde
       de `BaseETL`;
    2. importe-a aqui e registre no dicionario `REGISTRY`.

O CLI (`prometheus.cli`) usa este registro para listar e executar ETLs por nome.
"""

from __future__ import annotations

from prometheus.core.base_etl import BaseETL
from prometheus.etls.exemplo_avisos import AvisosDistribuicaoETL

REGISTRY: dict[str, type[BaseETL]] = {
    'avisos': AvisosDistribuicaoETL,
}

__all__ = ['REGISTRY', 'AvisosDistribuicaoETL']
