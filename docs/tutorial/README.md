# Tutorial do Prometheus

Este guia ensina a usar o **Prometheus**, um template para construir ETLs em Python
com conexões prontas para MongoDB e PostgreSQL.

A linguagem é propositalmente simples e direta: a meta é que o conteúdo seja claro o
suficiente para qualquer pessoa acompanhar, mesmo sem experiência prévia com o projeto.
Conceitos técnicos aparecem explicados na primeira vez que são usados.

---

## Por onde começar

Leia os capítulos na ordem. Cada um é um arquivo separado nesta pasta:

1. [O que é o Prometheus?](01-o-que-e.md)
   O conceito de ETL e por que usar um template.

2. [Preparando o ambiente](02-instalacao.md)
   Instalação passo a passo.

3. [Configuração](03-configuracao.md)
   Como apontar o projeto para seus bancos de dados.

4. [Criando sua primeira ETL](04-primeira-etl.md)
   Construindo um pipeline do zero.

5. [Executando](05-rodando.md)
   Rodando o pipeline e lendo os resultados.

6. [Solução de problemas](06-ajuda.md)
   Os erros mais comuns e como resolvê-los.

---

## Resumo rápido

Se você já leu uma vez e só quer relembrar os comandos:

```
1. Instalar   →  python -m venv .venv  e  pip install -e .
2. Configurar →  copiar .env.example para .env e preencher
3. Criar ETL  →  um arquivo novo em src/prometheus/etls/
4. Rodar      →  prometheus nome_da_etl --env dev
```

Comece pelo [capítulo 1](01-o-que-e.md).
