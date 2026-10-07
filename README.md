# Prometheus

Template limpo para construção de **ETLs** com conexões a **MongoDB** e **PostgreSQL**.

É a evolução da arquitetura de conexão/ETL usada no projeto Helios, reescrita como
um projeto base reutilizável: sem scripts avulsos, com configuração tipada,
conexões robustas e uma abstração de ETL pronta para estender.

## Por que usar

Melhorias em relação à arquitetura anterior:

| Antes (Helios) | Agora (Prometheus) |
| --- | --- |
| `config['CHAVE']` indexado no import → `KeyError` cru | `pydantic-settings` com validação e mensagens claras |
| `execute_query` engolia erros e retornava `[]` | erros são logados e **propagados** |
| `MongoDBManager` não era context manager de verdade | `MongoConnection` abre/fecha corretamente |
| Engine recriada a cada conexão | engine cacheada por URI (reuso do pool) |
| SQL por f-string (risco de injection) | consultas **parametrizadas** por padrão |
| Padrão "função por tabela + `main(ambiente)`" repetido | `BaseETL` formaliza extract → transform → load |

## Estrutura

```
prometheus/
├── pyproject.toml
├── .env.example            # modelo de variáveis de ambiente (copie para .env)
├── src/prometheus/
│   ├── config/settings.py  # configuração tipada por ambiente
│   ├── connections/
│   │   ├── mongo.py        # MongoConnection (context manager)
│   │   └── postgres.py     # PostgresConnection (context manager)
│   ├── core/
│   │   ├── base_etl.py     # BaseETL (extract/transform/load + run)
│   │   └── logging.py      # setup_logging idempotente
│   ├── etls/
│   │   ├── exemplo_avisos.py  # ETL de exemplo (modelo)
│   │   └── __init__.py        # REGISTRY de ETLs
│   └── cli.py              # executor por linha de comando
└── tests/
```

## Instalação

Usa o método padrão da documentação do Python: ambiente virtual com `venv` + `pip`
(sem Poetry). Rode os comandos a partir da pasta `prometheus/`.

**Windows (PowerShell):**

```powershell
cd prometheus
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt   # ou requirements.txt (apenas execução)
pip install -e .                      # instala o pacote em modo editável (habilita o comando `prometheus`)
Copy-Item .env.example .env           # depois edite com as credenciais reais
```

**Linux / macOS (bash):**

```bash
cd prometheus
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt   # ou requirements.txt (apenas execução)
pip install -e .                      # instala o pacote em modo editável (habilita o comando `prometheus`)
cp .env.example .env                  # depois edite com as credenciais reais
```

> O `pip install -e .` é opcional: ele habilita o comando `prometheus` e os imports
> `from prometheus import ...` de qualquer lugar. Sem ele, rode os módulos com
> `PYTHONPATH=src` (veja a seção **Executando**).

## Configuração

Toda a configuração vem do `.env` (veja `.env.example`). As URIs são definidas
por ambiente: `dev`, `tst`, `hml`, `preprod`, `prod`. O ambiente padrão é
controlado por `PROMETHEUS_ENV`.

```python
from prometheus import get_settings

settings = get_settings()
settings.mongo_uri('prod')      # URI do Mongo em prod
settings.postgres_uri('hml')    # URI do Postgres em hml
```

## Usando as conexões

```python
from prometheus import MongoConnection, PostgresConnection

# MongoDB (cursor preguiçoso, projeção)
with MongoConnection(environment='prod') as mongo:
    for doc in mongo.find('aviso', {'ativo': True}, {'_id': 0, 'numero': 1}):
        ...

# PostgreSQL (sempre parametrizado)
with PostgresConnection(environment='prod') as pg:
    linhas = pg.fetch_all(
        'SELECT * FROM processo WHERE criado_em >= :dt',
        {'dt': '2026-01-01'},
    )
    pg.execute('UPDATE processo SET ativo = true WHERE id = :id', {'id': 10})
```

## Criando uma ETL

1. Crie `src/prometheus/etls/minha_etl.py` com uma classe que herde de `BaseETL`
   e implemente `extract`, `transform` (opcional) e `load`.
2. Registre no `REGISTRY` em `src/prometheus/etls/__init__.py`.

```python
from prometheus.core.base_etl import BaseETL

class MinhaETL(BaseETL):
    name = 'minha_etl'

    def extract(self):
        ...

    def transform(self, data):
        return data

    def load(self, data):
        ...
```

## Executando

Com o ambiente virtual ativado:

```bash
# Se você rodou `pip install -e .`, o comando `prometheus` fica disponível:
prometheus --list                   # lista ETLs registradas
prometheus avisos --env prod        # roda a ETL "avisos" em prod
prometheus avisos --env prod hml    # vários ambientes

# Alternativa sem instalar o pacote (defina o PYTHONPATH para a pasta src):
#   PowerShell:  $env:PYTHONPATH="src"; python -m prometheus.cli avisos --env prod
#   bash:        PYTHONPATH=src python -m prometheus.cli avisos --env prod

# Ou rode o módulo da ETL diretamente:
python -m prometheus.etls.exemplo_avisos
```

## Testes

Com o ambiente virtual ativado (o `pytest` já lê `pythonpath = ["src"]` do `pyproject.toml`):

```bash
pytest
```

## Segurança

- **Nunca** faça commit do `.env` com credenciais reais (ele está no `.gitignore`).
- Todas as consultas SQL devem ser parametrizadas — nunca interpole valores em f-strings.
