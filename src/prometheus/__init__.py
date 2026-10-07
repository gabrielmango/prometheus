"""Prometheus - template limpo para construcao de ETLs.

Expoe os pontos de entrada mais usados no nivel do pacote para imports curtos:

    from prometheus import BaseETL, get_settings, MongoConnection, PostgresConnection
"""

from prometheus.config.settings import Environment, Settings, get_settings
from prometheus.connections.mongo import MongoConnection
from prometheus.connections.postgres import PostgresConnection
from prometheus.core.base_etl import BaseETL

__all__ = [
    'BaseETL',
    'Environment',
    'MongoConnection',
    'PostgresConnection',
    'Settings',
    'get_settings',
]

__version__ = '0.1.0'
