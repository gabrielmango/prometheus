# 6. Solução de problemas

Encontrou um erro? É normal. Abaixo estão os problemas mais comuns e como resolvê-los.

---

## "O comando `prometheus` não funciona"

**Mensagem típica:** algo como `'prometheus' não é reconhecido...`

**Causa:** ou o ambiente virtual não está ativo, ou faltou instalar o pacote em modo
editável.

**Solução:**

1. Verifique se há `(.venv)` no início da linha do terminal. Se não houver, ative o ambiente:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
2. Se o problema persistir, reinstale o pacote em modo editável:
   ```powershell
   pip install -e .
   ```

---

## "URI do MongoDB não configurada para o ambiente..."

**Mensagem típica:** `URI do MongoDB nao configurada para o ambiente "dev"`.

**Causa:** o projeto não encontrou o endereço do banco. Ou o `.env` não existe, ou a
variável do ambiente em questão está vazia.

**Solução:**

1. Confirme que o arquivo `.env` existe. Se não, crie-o (veja o [capítulo 3](03-configuracao.md)):
   ```powershell
   Copy-Item .env.example .env
   ```
2. Abra o `.env` e preencha a variável correspondente ao ambiente. Para o `dev`, por
   exemplo, preencha a linha `MONGO_URI_DEV=` com o endereço correto.

> A mensagem de erro indica exatamente qual variável preencher (por exemplo,
> `Defina MONGO_URI_DEV no seu .env`). Vale ler o texto com atenção.

---

## "Ambiente invalido"

**Mensagem típica:** `Ambiente invalido: "..."`.

**Causa:** o nome de ambiente informado não existe.

**Solução:** use apenas um destes valores:

```
dev   tst   hml   preprod   prod
```

Exemplo correto:
```powershell
prometheus minha_primeira --env dev
```

---

## "ETL desconhecida"

**Mensagem típica:** `ETL desconhecida: "..."`.

**Causa:** o nome informado não está no registro de ETLs.

**Solução:**

1. Liste as ETLs existentes:
   ```powershell
   prometheus --list
   ```
2. Use um nome exatamente como aparece na lista.
3. Se a sua ETL não aparece, ela não foi registrada no `REGISTRY`. Volte ao
   [capítulo 4, passo 3](04-primeira-etl.md).

---

## "python não é reconhecido"

**Causa:** o Python não está instalado ou não está no PATH do sistema.

**Solução:**

1. Instale o Python a partir de [python.org](https://www.python.org/downloads/).
2. No Windows, durante a instalação, marque a opção **"Add Python to PATH"**.

---

## Rodando os testes

O projeto inclui testes automatizados, úteis para confirmar que nada quebrou:

```powershell
pytest
```

Se os testes passarem (a saída mostra `passed`), o projeto está íntegro.

---

## Verificando o estilo do código (opcional)

O **ruff** analisa e padroniza o estilo do código automaticamente:

```powershell
ruff check .
```

---

## Ainda com problema?

1. **Leia a mensagem de erro com atenção.** Com frequência ela já indica a solução.
2. **Consulte os logs** na pasta `logs/`. Costuma haver pistas sobre o que ocorreu.
3. **Peça ajuda** à sua equipe, incluindo a mensagem de erro completa — isso acelera
   bastante o diagnóstico.

---

Quer rever algo? Volte ao [índice do tutorial](README.md).
