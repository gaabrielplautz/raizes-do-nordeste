from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

# --- Schemas de Usuário ---
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo: Optional[str] = "CLIENTE"

    @field_validator('tipo', mode='before')
    @classmethod
    def converter_para_maiusculo(cls, v):
        """Converte automaticamente qualquer tipo de usuário para maiúsculas (ex: 'cliente' -> 'CLIENTE')"""
        if isinstance(v, str):
            return v.upper()
        return v

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