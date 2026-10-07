"""Configuracao de logging.

Melhora o antigo `setup_logging.py`:

- idempotente (chamar varias vezes nao duplica handlers);
- usa `logging.getLogger(name)` em vez de `basicConfig` global;
- grava em `logs/AAAA_MM_DD/<nome>.log` e tambem no console.
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

_LOG_FORMAT = '%(asctime)s | %(levelname)-7s | %(name)s | %(message)s'


def setup_logging(name: str, level: str = 'INFO', log_dir: str | Path = 'logs') -> logging.Logger:
    """Configura e retorna um logger nomeado, com saida em arquivo e console.

    Args:
        name: nome do logger/arquivo (ex.: o nome da ETL).
        level: nivel de log (DEBUG, INFO, WARNING, ERROR).
        log_dir: diretorio base para os arquivos de log.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Evita handlers duplicados em re-execucoes dentro do mesmo processo.
    if logger.handlers:
        return logger

    date_folder = datetime.now().strftime('%Y_%m_%d')
    target_dir = Path(log_dir) / date_folder
    target_dir.mkdir(parents=True, exist_ok=True)
    log_file = target_dir / f'{name}.log'

    formatter = logging.Formatter(_LOG_FORMAT)

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger
