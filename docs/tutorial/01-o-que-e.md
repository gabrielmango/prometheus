# 1. O que é o Prometheus?

## O conceito de ETL

Imagine que você precisa pegar os brinquedos espalhados numa caixa (o lugar A) e
guardá-los organizados numa estante na sala (o lugar B). O trabalho se divide em
três etapas:

1. **Pegar** os brinquedos da caixa → chamamos de **Extract** (extrair)
2. **Organizar** por cor e tamanho → chamamos de **Transform** (transformar)
3. **Guardar** na estante → chamamos de **Load** (carregar)

Pegar → Organizar → Guardar. Em inglês: **E**xtract → **T**ransform → **L**oad.
Juntando as iniciais, temos **ETL**.

> **ETL** é o nome do processo de ler dados de uma origem, ajustá-los e gravá-los
> em um destino. É um padrão muito comum em projetos de dados.

## O que o Prometheus faz

O Prometheus é um **template**: um ponto de partida pronto, como uma forma de bolo.
Você não refaz a estrutura toda vez; ela já existe, e você preenche só o que muda.

O que já vem pronto no projeto:

- **Conexões com bancos de dados.** Ele sabe se comunicar com dois tipos de banco:
  **MongoDB** e **PostgreSQL** (dois lugares diferentes onde dados ficam guardados).
- **Registro de execução (logs).** Um histórico de tudo que aconteceu durante a execução.
- **Uma estrutura base para ETLs.** Um esqueleto que você estende para criar seus
  pipelines rapidamente, sem reescrever a parte repetitiva.

## O que você vai construir com ele

Você vai criar pequenos pipelines (as ETLs) que:

1. Leem dados de uma origem (por exemplo, o MongoDB)
2. Ajustam esses dados ao formato desejado
3. Gravam no destino (por exemplo, o PostgreSQL)

O ganho do template é que ele cuida da parte repetitiva e sujeita a erro — abrir e
fechar conexões, registrar logs, medir tempo e tratar falhas. Você se concentra no que
é específico do seu caso: **o que** extrair, **como** transformar e **onde** carregar.

---

Com o conceito claro, vamos preparar o ambiente no [capítulo 2](02-instalacao.md).
