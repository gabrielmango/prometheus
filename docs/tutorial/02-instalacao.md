# 2. Preparando o ambiente

Antes de usar o projeto, é preciso preparar o ambiente. Faça um passo de cada vez.

## Pré-requisitos

- Um computador com terminal (PowerShell no Windows, ou bash no Mac/Linux).
- **Python 3.11 ou mais novo** instalado. Python é a linguagem em que o Prometheus é escrito.

### Verificando se o Python está instalado

Abra o terminal e execute:

```powershell
python --version
```

Se aparecer algo como `Python 3.11.5`, está tudo certo. Caso contrário, instale o
Python a partir do site oficial: [python.org](https://www.python.org/downloads/).

## Instalação passo a passo

> Os comandos abaixo são para **Windows (PowerShell)**. A versão para Mac/Linux está no
> fim da página.

### Passo 1 — Entrar na pasta do projeto

```powershell
cd prometheus
```

`cd` significa "change directory" (mudar de diretório).

### Passo 2 — Criar um ambiente virtual

```powershell
python -m venv .venv
```

Isso cria um **ambiente virtual**: um espaço isolado só para este projeto.

> Por que isso importa: as dependências instaladas aqui ficam separadas das de outros
> projetos, evitando conflitos de versão entre eles.

### Passo 3 — Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Depois disso, aparece um `(.venv)` no início da linha do terminal, indicando que o
ambiente está ativo.

### Passo 4 — Atualizar o instalador de pacotes

```powershell
python -m pip install --upgrade pip
```

O `pip` é a ferramenta que instala as dependências do projeto. Aqui apenas garantimos
que ele esteja atualizado.

### Passo 5 — Instalar as dependências

```powershell
pip install -r requirements-dev.txt
```

Isso baixa e instala tudo que o projeto precisa. Pode levar um ou dois minutos.

> Existem dois arquivos de dependências:
> - `requirements-dev.txt` — tudo, inclusive as ferramentas de desenvolvimento (testes, lint).
> - `requirements.txt` — apenas o necessário para executar o projeto.
>
> Para desenvolver e aprender, use o `-dev`.

### Passo 6 — Instalar o pacote em modo editável

```powershell
pip install -e .
```

Isso disponibiliza o comando `prometheus` no terminal e habilita os imports
`from prometheus import ...` a partir de qualquer lugar.

---

## No Mac ou Linux

Quase idêntico; mudam apenas dois comandos:

```bash
cd prometheus
python3 -m venv .venv
source .venv/bin/activate          # ativação do ambiente
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .
```

---

## Verificando se deu certo

Execute:

```powershell
prometheus --list
```

Se aparecer uma lista de ETLs (por exemplo, `- avisos`), a instalação foi concluída
com sucesso. Se ocorrer algum erro, consulte o [capítulo 6 (Solução de problemas)](06-ajuda.md).

---

Com o ambiente pronto, vamos à configuração no [capítulo 3](03-configuracao.md).
