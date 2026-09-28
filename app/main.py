from fastapi import FastAPI
from app.core.database import engine, Base
from app.api import auth

# Cria as tabelas no banco de dados SQLite com base nos modelos ORM
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Raízes do Nordeste API",
    description="Backend oficial da rede Raízes do Nordeste desenvolvido em FastAPI para a Uninter.",
    version="1.0.0"
)

# Inclui as rotas de autenticação
app.include_router(auth.router)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "projeto": "Raízes do Nordeste API",
        "status": "online",
        "documentacao": "/docs"
    }