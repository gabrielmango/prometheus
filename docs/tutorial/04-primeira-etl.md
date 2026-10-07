# 4. Criando sua primeira ETL

Agora vamos construir um pipeline (uma ETL) do zero. Lembre do conceito do capítulo 1:
Pegar → Organizar → Guardar.

## A estrutura de uma ETL

Toda ETL no Prometheus tem três etapas, que correspondem às letras de ETL:

| Etapa | O que faz | Analogia dos brinquedos |
| --- | --- | --- |
| `extract` | **Lê** os dados da origem | Pegar os brinquedos da caixa |
| `transform` | **Ajusta** os dados | Organizar por cor e tamanho |
| `load` | **Grava** os dados no destino | Guardar na estante |

> O `transform` é **opcional**. Se não há nada a ajustar, os dados passam direto da
> extração para a carga.

## Um exemplo pronto

O projeto já traz uma ETL de exemplo em `src/prometheus/etls/exemplo_avisos.py`. A
estrutura dela, resumida, é esta:

```python
from prometheus.core.base_etl import BaseETL

class AvisosDistribuicaoETL(BaseETL):
    name = 'avisos_distribuicao'

    def extract(self):
        # 1. Lê os dados do MongoDB
        ...

    def transform(self, data):
        # 2. Ajusta os dados
        ...

    def load(self, data):
        # 3. Grava os dados no PostgreSQL
        ...
```

São as três etapas: `extract`, `transform` e `load`.

## Criando a sua

Vamos criar uma ETL simples, só para praticar: ela lê alguns números, multiplica cada
um por 2 e mostra o resultado.

### Passo 1 — Criar o arquivo

Crie um arquivo chamado `minha_primeira_etl.py` dentro de:

```
src/prometheus/etls/
```

### Passo 2 — Escrever o pipeline

Coloque este conteúdo no arquivo:

```python
from prometheus.core.base_etl import BaseETL


class MinhaPrimeiraETL(BaseETL):
    name = 'minha_primeira'

    def extract(self):
        # Lê os dados: aqui, uma lista fixa de números
        numeros = [1, 2, 3, 4, 5]
        self.logger.info('Peguei os números: %s', numeros)
        return numeros

    def transform(self, data):
        # Ajusta: multiplica cada número por 2
        dobrados = [n * 2 for n in data]
        self.logger.info('Dobrei os números: %s', dobrados)
        return dobrados

    def load(self, data):
        # Grava: aqui, apenas exibe o resultado
        self.logger.info('Resultado final: %s', data)
        return data
```

### Passo 3 — Registrar a ETL

O Prometheus mantém um **registro** das ETLs conhecidas. É preciso adicionar a sua lá;
caso contrário o executor não sabe que ela existe.

O registro fica em `src/prometheus/etls/__init__.py`. Deixe-o parecido com isto:

```python
from prometheus.core.base_etl import BaseETL
from prometheus.etls.exemplo_avisos import AvisosDistribuicaoETL
from prometheus.etls.minha_primeira_etl import MinhaPrimeiraETL   # adicione esta linha

REGISTRY: dict[str, type[BaseETL]] = {
    'avisos': AvisosDistribuicaoETL,
    'minha_primeira': MinhaPrimeiraETL,   # e esta linha
}
```

> O `REGISTRY` funciona como uma lista de nomes conhecidos. O executor só reconhece o
> que está nessa lista. A chave à esquerda (`'minha_primeira'`) é o nome que você usa
> na linha de comando para rodar a ETL.

## O que você aprendeu

- Toda ETL tem três etapas: `extract`, `transform` e `load`.
- Você implementa cada etapa dizendo o que ela deve fazer.
- Depois, registra a ETL no `REGISTRY` para que o executor a reconheça.

Repare no principal benefício: você não precisou tratar conexões, medir tempo nem
configurar logs manualmente. A classe base (`BaseETL`) cuida disso. Você escreveu
apenas a lógica específica do seu pipeline.

---

Pipeline criado. Vamos executá-lo no [capítulo 5](05-rodando.md).
