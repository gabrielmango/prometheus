"""Abstracao base para ETLs.

Formaliza o padrao dominante do projeto antigo ("funcao por tabela,
`main(ambiente)`, loop de ambientes no final") numa classe reutilizavel com
tres etapas explicitas: extract -> transform -> load.

Uma ETL concreta so precisa herdar de `BaseETL` e implementar `extract`,
(opcionalmente) `transform` e `load`. O metodo `run()` orquestra tudo,
cuida do logging, cronometra a execucao e trata erros de forma consistente.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any

from prometheus.config.settings import Environment, Settings, get_settings
from prometheus.core.logging import setup_logging


class BaseETL(ABC):
    """Classe base para pipelines de ETL.

    Attributes:
        name: identificador da ETL (usado em logs e nome de arquivo de log).
        environment: ambiente alvo (dev/tst/hml/preprod/prod).
    """

    #: Nome da ETL. Sobrescreva na subclasse ou passe no __init__.
    name: str = 'etl'

    def __init__(
        self,
        environment: Environment | str | None = None,
        *,
        name: str | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.environment = self.settings._coerce_env(environment)
        if name:
            self.name = name
        self.logger = setup_logging(self.name, level=self.settings.log_level)

    # Etapas do ETL -----------------------------------------------------------
    @abstractmethod
    def extract(self) -> Any:
        """Extrai os dados da origem. Retorna o dado bruto para o transform."""
        raise NotImplementedError

    def transform(self, data: Any) -> Any:
        """Transforma os dados extraidos. Por padrao, repassa sem alteracao."""
        return data

    @abstractmethod
    def load(self, data: Any) -> Any:
        """Carrega os dados no destino. Retorna um resumo (ex.: nº de linhas)."""
        raise NotImplementedError

    # Orquestracao ------------------------------------------------------------
    def run(self) -> Any:
        """Executa extract -> transform -> load com logging e cronometragem."""
        self.logger.info('==> Iniciando ETL "%s" (ambiente=%s).', self.name, self.environment)
        inicio = time.perf_counter()
        try:
            dados = self.extract()
            self.logger.info('Extract concluido.')

            dados = self.transform(dados)
            self.logger.info('Transform concluido.')

            resultado = self.load(dados)
            self.logger.info('Load concluido: %s', resultado)
        except Exception:
            self.logger.exception('ETL "%s" falhou (ambiente=%s).', self.name, self.environment)
            raise
        else:
            duracao = time.perf_counter() - inicio
            self.logger.info('==> ETL "%s" finalizada em %.2fs.', self.name, duracao)
            return resultado
