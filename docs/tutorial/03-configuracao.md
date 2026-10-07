# 3. Configuração

Para o Prometheus ler e gravar dados, ele precisa saber **onde** ficam os bancos de
dados e **com quais credenciais** acessá-los. Essas informações ficam num arquivo
chamado **`.env`**.

> O `.env` é o arquivo de configuração sensível do projeto: guarda endereços e senhas
> dos bancos. Trate-o como um cofre.

## Passo 1 — Copiar o modelo

O projeto já inclui um modelo chamado `.env.example`. Faça uma cópia dele com o nome `.env`:

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

**Mac ou Linux:**

```bash
cp .env.example .env
```

## Passo 2 — Abrir e preencher

Abra o `.env` no seu editor. Ele contém linhas como estas:

```bash
PROMETHEUS_ENV=dev
LOG_LEVEL=INFO

MONGO_URI_DEV=mongodb://usuario:senha@localhost:27017/?authSource=admin
POSTGRES_URI_DEV=postgresql+psycopg2://usuario:senha@localhost:5432/app_db
```

### O que cada variável significa

| Variável | Significado |
| --- | --- |
| `PROMETHEUS_ENV` | O ambiente usado por padrão quando nenhum é informado. |
| `LOG_LEVEL` | O nível de detalhe das mensagens de log. |
| `MONGO_URI_...` | Endereço e credenciais do MongoDB. |
| `POSTGRES_URI_...` | Endereço e credenciais do PostgreSQL. |

### Os ambientes

O projeto trabalha com cinco ambientes, cada um com suas próprias URIs. Isso evita
misturar dados de teste com dados reais:

- **`dev`** — desenvolvimento. É onde você começa e testa à vontade.
- **`tst`** — testes.
- **`hml`** — homologação (ensaio geral antes de ir para produção).
- **`preprod`** — pré-produção, bem próximo do ambiente real.
- **`prod`** — produção, com dados reais. Exige cuidado redobrado.

> Repare que cada ambiente tem a sua variável. `MONGO_URI_DEV` aponta para o banco de
> desenvolvimento e `MONGO_URI_PROD` para o de produção. Assim os ambientes nunca se misturam.

### Níveis de log (`LOG_LEVEL`)

Controla o quanto o programa registra:

- `DEBUG` — tudo, incluindo detalhes internos. Útil ao investigar problemas.
- `INFO` — as mensagens relevantes (padrão).
- `WARNING` — apenas avisos.
- `ERROR` — apenas erros graves.

Para começar, mantenha em `INFO`.

## Passo 3 — Substituir pelos valores reais

Nas URIs, troque `usuario`, `senha`, `localhost` e as portas pelos valores reais do
seu banco. Por exemplo, para um MongoDB local com usuário `joao` e senha `banana123`:

```bash
MONGO_URI_DEV=mongodb://joao:banana123@localhost:27017/?authSource=admin
```

> Se você não tem esses valores, peça à pessoa responsável pelos bancos de dados na sua
> equipe. Ela fornece o endereço e as credenciais corretas.

## Regra de segurança essencial

**Nunca** compartilhe o seu `.env` nem o publique em repositórios ou na internet. Ele
contém credenciais reais, equivalentes às chaves de acesso aos bancos.

> O projeto já está configurado para ignorar o `.env` no controle de versão (ele está
> listado no `.gitignore`), de modo que não vai parar num commit por acidente.

---

Com a configuração pronta, vamos criar uma ETL no [capítulo 4](04-primeira-etl.md).
