"""Interface de linha de comando para rodar ETLs.

Permite executar uma ETL registrada por nome e para um ou mais ambientes:

    poetry run prometheus avisos --env prod
    poetry run prometheus avisos --env prod hml
    poetry run prometheus --list
"""

from __future__ import annotations

import argparse
import sys

from prometheus.config.settings import Environment
from prometheus.etls import REGISTRY


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='prometheus', description='Executor de ETLs do template Prometheus.')
    parser.add_argument('etl', nargs='?', help='Nome da ETL a executar (veja --list).')
    parser.add_argument(
        '--env',
        nargs='+',
        default=['dev'],
        choices=[e.value for e in Environment],
        help='Um ou mais ambientes (padrao: dev).',
    )
    parser.add_argument('--list', action='store_true', help='Lista as ETLs disponiveis e sai.')
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.list or not args.etl:
        print('ETLs disponiveis:')
        for nome in sorted(REGISTRY):
            print(f'  - {nome}')
        return 0

    if args.etl not in REGISTRY:
        print(f'ETL desconhecida: "{args.etl}". Use --list para ver as opcoes.', file=sys.stderr)
        return 1

    etl_cls = REGISTRY[args.etl]
    for env in args.env:
        etl_cls(environment=env).run()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
