from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Schemas de Usuário ---
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo: Optional[str] = "cliente"

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    tipo: str

    class Config:
        from_attributes = True

# --- Schemas de Autenticação ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Schemas de Produto ---
class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade_inicial: int = 0

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    preco: float

    class Config:
        from_attributes = True

# --- Schemas de Estoque ---
class EstoqueUpdate(BaseModel):
    quantidade: int