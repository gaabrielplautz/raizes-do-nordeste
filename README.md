# Raízes do Nordeste - API Backend (Uninter)

API RESTful desenvolvida em Python com FastAPI para gerir o sistema multicanal de pedidos, controlo de stock por unidade, autenticação JWT e simulação de pagamentos da rede "Raízes do Nordeste".

---

## 🛠️ Tecnologias e Stack
- **Linguagem:** Python 3.10+
- **Framework Web:** FastAPI
- **ORM / Persistência:** SQLAlchemy (SQLite)
- **Validação de Dados:** Pydantic
- **Servidor ASGI:** Uvicorn

---

## 📂 Estrutura do Projeto
```text
raizes-do-nordeste-backend/
├── app/
│   ├── api/          # Endpoints / Rotas (Auth, Produtos, Pedidos, Pagamentos, Canais)
│   ├── core/         # Configurações, Base de Dados e Segurança (JWT)
│   ├── models/       # Modelos SQLAlchemy (Entidades do Banco de Dados)
│   ├── schemas/      # Schemas Pydantic (Validação de Request/Response)
│   └── services/     # Regras de Negócio e Lógica de Aplicação
├── postman/          # Coleção de Testes em JSON (.json)
├── run.py            # Ponto de entrada para execução da API
├── requirements.txt  # Dependências do projeto
└── .env.example      # Exemplo de variáveis de ambiente