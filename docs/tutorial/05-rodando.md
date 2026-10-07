# 5. Executando

Hora de rodar o pipeline que você criou.

> **Antes de tudo:** você precisa estar com o ambiente virtual ativo. Se o `(.venv)`
> não aparecer no início da linha, ative novamente:
>
> ```powershell
> .\.venv\Scripts\Activate.ps1
> ```

## Listar as ETLs disponíveis

Primeiro, veja quais ETLs estão registradas:

```powershell
prometheus --list
```

A saída será parecida com:

```
ETLs disponiveis:
  - avisos
  - minha_primeira
```

Se o `minha_primeira` (que você registrou no capítulo anterior) aparecer, está tudo certo.

## Executar sua ETL

Basta chamar a ETL pelo nome registrado:

```powershell
prometheus minha_primeira --env dev
```

Entendendo cada parte do comando:

| Parte | Significado |
| --- | --- |
| `prometheus` | O executor de ETLs do projeto. |
| `minha_primeira` | O nome registrado da ETL que você quer rodar. |
| `--env dev` | O ambiente de execução (aqui, desenvolvimento). |

> O `--env` usa os ambientes vistos no capítulo 3. `--env dev` roda em desenvolvimento;
> `--env prod` rodaria em produção, o que exige cuidado.

## O que aparece na tela

Como a ETL de exemplo escreve logs, a saída será parecida com:

```
... | INFO | minha_primeira | ==> Iniciando ETL "minha_primeira" (ambiente=dev).
... | INFO | minha_primeira | Peguei os números: [1, 2, 3, 4, 5]
... | INFO | minha_primeira | Dobrei os números: [2, 4, 6, 8, 10]
... | INFO | minha_primeira | Resultado final: [2, 4, 6, 8, 10]
... | INFO | minha_primeira | ==> ETL "minha_primeira" finalizada em 0.01s.
```

A ETL leu os números `[1, 2, 3, 4, 5]`, dobrou para `[2, 4, 6, 8, 10]`, mostrou o
resultado e ainda informou quanto tempo levou. Seu primeiro pipeline funcionou.

## Onde ficam os logs

O Prometheus grava um registro de cada execução em arquivos, dentro da pasta `logs/`,
organizados por data:

```
logs/
└── 2026_10_07/              <- data da execução
    └── minha_primeira.log   <- log desta ETL
```

> Esses arquivos são valiosos para diagnóstico: se algo falhar depois, você abre o log e
> vê exatamente o que aconteceu.

## Outras formas de executar

### Rodar em vários ambientes de uma vez

```powershell
prometheus minha_primeira --env dev hml
```

Executa a ETL primeiro em `dev` e depois em `hml`.

### Rodar sem o comando instalado

Se o comando `prometheus` não estiver disponível, você pode rodar pelo módulo:

```powershell
$env:PYTHONPATH="src"; python -m prometheus.cli minha_primeira --env dev
```

É mais verboso, mas tem o mesmo efeito.

---

Deu tudo certo? Ótimo. Se encontrou algum erro, veja o
[capítulo 6 (Solução de problemas)](06-ajuda.md).
