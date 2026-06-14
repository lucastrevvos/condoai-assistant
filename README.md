# CondoAI Assistant

Assistente conversacional para condomínios, integrando Telegram, FastAPI, PostgreSQL e serviços AWS para automatizar atendimentos operacionais e fluxo de documentos.

## Visão geral

O CondoAI Assistant é uma API backend para atendimento de moradores via Telegram. O projeto organiza mensagens por intenção, responde dúvidas operacionais, consulta boletos próximos ao vencimento e oferece uma base para processamento assíncrono de documentos enviados por moradores ou administração.

A proposta é aproximar tarefas comuns de gestão condominial de uma experiência simples de chat, mantendo uma arquitetura extensível para integrações com banco de dados, armazenamento de arquivos, filas e modelos de linguagem.

## Problema

Administradoras e síndicos lidam diariamente com perguntas repetitivas, solicitações sobre boletos, comunicados aos moradores e documentos como atas, anexos e arquivos internos. Quando essas demandas ficam espalhadas em canais manuais, o atendimento tende a consumir tempo operacional e dificultar a organização do histórico.

## Solução

O projeto centraliza esse atendimento em um assistente conectado ao Telegram. As mensagens recebidas passam por um roteador de intenções que direciona cada solicitação para agentes especializados em suporte, financeiro ou documentos.

Além do webhook de mensagens, a aplicação possui um endpoint de upload que armazena documentos no S3, registra metadados no PostgreSQL e enfileira o processamento via SQS. Um worker separado consome a fila, recupera o arquivo, extrai texto de PDFs ou arquivos TXT, gera um resumo inicial e envia a resposta ao chat de origem.

## Funcionalidades

- Webhook para receber mensagens do Telegram.
- Roteamento de intenções por regras e fallback opcional com OpenAI.
- Agente financeiro com consulta de boletos a vencer nos próximos dias.
- Agente de suporte com resposta inicial e geração de comunicado padrão para moradores.
- Agente de documentos para direcionamento de solicitações relacionadas a arquivos.
- Endpoint HTTP para upload de documentos.
- Armazenamento de documentos em bucket S3.
- Registro de documentos e boletos em PostgreSQL via SQLAlchemy.
- Enfileiramento de jobs de documentos com AWS SQS.
- Worker assíncrono para processamento de documentos.
- Extração de texto de PDFs e arquivos TXT.
- Resumo inicial de conteúdo textual extraído.
- Endpoint de health check para verificação da API.
- Seed de dados para popular boletos de exemplo no banco local.

## Stack

- Python
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Pydantic
- Telegram Bot API
- OpenAI API
- AWS S3
- AWS SQS
- boto3
- httpx
- pypdf
- Docker Compose
- python-dotenv

## Arquitetura

A aplicação é organizada em camadas simples, com separação entre entrada HTTP, regras de roteamento, agentes de domínio, serviços de infraestrutura e processamento assíncrono.

```text
app/
├── agents/        # Roteador de intenções e agentes especializados
├── core/          # Configuração por variáveis de ambiente
├── domain/        # Modelos persistidos no banco
├── infra/         # Clientes de infraestrutura: banco, S3 e SQS
├── services/      # Casos de uso e integrações de aplicação
├── telegram/      # Schemas e cliente da Telegram Bot API
└── main.py        # API FastAPI, health check, upload e webhook

workers/
└── document_worker.py  # Consumidor SQS para processamento de documentos

scripts/
└── seed_db.py          # Inicialização de tabelas e dados de exemplo
```

O fluxo principal funciona da seguinte forma:

1. O Telegram envia mensagens para `POST /webhook/telegram`.
2. O roteador classifica a intenção da mensagem.
3. O agente correspondente gera a resposta.
4. A resposta é enviada de volta ao usuário pela Telegram Bot API.

O fluxo de documentos segue um caminho assíncrono:

1. Um arquivo é enviado para `POST /upload` com o `chat_id`.
2. A API salva o arquivo no S3 e registra o documento no PostgreSQL.
3. Um job é publicado no SQS.
4. O worker consome a mensagem, processa o documento e atualiza o registro.
5. O resultado é enviado ao chat no Telegram.

## Como rodar

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd condoai-assistant
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Suba o PostgreSQL local

```bash
docker compose up -d db
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis listadas na seção [Configuração](#configuração).

### 6. Inicialize dados de exemplo

```bash
python scripts/seed_db.py
```

### 7. Inicie a API

```bash
python -m uvicorn app.main:app --reload --port 8000
```

A API ficará disponível em:

```text
http://localhost:8000
```

Para validar a aplicação:

```bash
curl http://localhost:8000/health
```

### 8. Execute o worker de documentos

Em outro terminal, com o ambiente virtual ativo:

```bash
python workers/document_worker.py
```

### 9. Configure o webhook do Telegram

Durante o desenvolvimento local, exponha a API com uma ferramenta como ngrok e configure o webhook do Telegram apontando para:

```text
https://<seu-dominio-publico>/webhook/telegram
```

## Configuração

Variáveis de ambiente usadas pela aplicação:

```env
TELEGRAM_BOT_TOKEN=
DATABASE_URL=
OPENAI_API_KEY=
OPENAI_MODEL=
AWS_REGION=
AWS_S3_BUCKET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SQS_QUEUE_URL=
```

Observações:

- `TELEGRAM_BOT_TOKEN` é usado para integração com a Telegram Bot API.
- `DATABASE_URL` define a conexão com o PostgreSQL.
- `OPENAI_API_KEY` habilita o fallback de classificação por modelo de linguagem.
- `OPENAI_MODEL` permite selecionar o modelo usado na classificação de intenção.
- `AWS_REGION`, `AWS_S3_BUCKET` e credenciais AWS conectam o upload ao S3.
- `AWS_SQS_QUEUE_URL` conecta a API e o worker à fila de processamento.

## Decisões técnicas

- **FastAPI como camada HTTP:** oferece uma base objetiva para criar endpoints assíncronos, validar payloads e expor a API com baixa cerimônia.
- **Telegram como interface conversacional:** simplifica o acesso do usuário final sem exigir uma aplicação frontend dedicada.
- **Roteamento híbrido de intenções:** combina regras explícitas para casos comuns com fallback opcional usando OpenAI para mensagens menos diretas.
- **Agentes por domínio:** separa responsabilidades entre suporte, financeiro e documentos, facilitando evolução incremental.
- **PostgreSQL com SQLAlchemy:** fornece persistência relacional para boletos e documentos com modelos claros de domínio.
- **S3 para armazenamento de arquivos:** mantém documentos fora do banco de dados e preserva metadados na aplicação.
- **SQS com worker separado:** desacopla upload e processamento, permitindo que documentos sejam tratados em segundo plano.
- **Configuração por ambiente:** concentra tokens, conexões e integrações externas em variáveis de ambiente, sem valores sensíveis versionados.

## Status

O projeto está em estágio funcional de portfólio, com API, webhook, roteamento de mensagens, consulta financeira, upload de documentos, persistência e worker assíncrono implementados. A base atual demonstra um fluxo completo de atendimento conversacional e processamento de arquivos, mantendo espaço para evoluções de produto e integrações adicionais.

## Roadmap

- Evoluir o agente de documentos para respostas mais completas a partir do conteúdo processado.
- Adicionar histórico conversacional por morador ou condomínio.
- Expandir o módulo financeiro com filtros por unidade, status e período.
- Criar autenticação administrativa para endpoints internos.
- Adicionar testes automatizados para agentes, serviços e endpoints principais.
- Publicar instruções de deploy em ambiente cloud.
- Melhorar observabilidade com logs estruturados e métricas de processamento.

## O que este projeto demonstra

- Construção de APIs com FastAPI.
- Integração com Telegram Bot API.
- Modelagem relacional com SQLAlchemy e PostgreSQL.
- Uso de filas para processamento assíncrono.
- Integração com AWS S3 e AWS SQS.
- Organização de backend em camadas.
- Separação de responsabilidades por agentes e serviços.
- Uso de variáveis de ambiente para configuração segura.
- Aplicação prática de LLM como fallback em classificação de intenção.
- Desenho de uma solução orientada a produto para automação operacional.
