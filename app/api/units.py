from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.models.models import Unidade
from app.models.product import Product, Stock  # <--- Importa o Stock do mesmo sítio que os produtos

router = APIRouter(prefix="/unidades", tags=["Gestão de Unidades e Cardápio"])

# --- Schemas para Unidades e Cardápio ---
class UnidadeCreate(BaseModel):
    nome: str
    endereco: str | None = None
    ativa: bool = True

class UnidadeResponse(BaseModel):
    id: int
    nome: str
    endereco: str | None
    ativa: bool

    class Config:
        from_attributes = True

class ProdutoCardapioResponse(BaseModel):
    produto_id: int
    nome: str
    descricao: str | None
    preco: float
    quantidade_em_estoque: int

    class Config:
        from_attributes = True


# --- Endpoints ---

@router.post("/", response_model=UnidadeResponse, status_code=status.HTTP_201_CREATED)
def criar_unidade(unidade_data: UnidadeCreate, db: Session = Depends(get_db)):
    """Cadastra uma nova unidade da rede (RF02)."""
    nova_unidade = Unidade(
        nome=unidade_data.nome,
        endereco=unidade_data.endereco,
        ativa=unidade_data.ativa
    )
    db.add(nova_unidade)
    db.commit()
    db.refresh(nova_unidade)
    return nova_unidade


@router.get("/", response_model=List[UnidadeResponse])
def listar_unidades(db: Session = Depends(get_db)):
    """Lista todas as unidades da rede (RF02)."""
    return db.query(Unidade).all()


@router.get("/{unit_id}/cardapio", response_model=List[ProdutoCardapioResponse])
def obter_cardapio_por_unidade(unit_id: int, db: Session = Depends(get_db)):
    """
    Retorna o cardápio/produtos disponíveis filtrados estritamente pela unidade informada (RF02).
    """
    # Verifica se a unidade existe
    unidade = db.query(Unidade).filter(Unidade.id == unit_id).first()
    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unidade com ID {unit_id} não encontrada."
        )

    # Busca os produtos associados ao estoque desta unidade usando a classe Stock unificada
    resultados = (
        db.query(Product, Stock.quantity)
        .join(Stock, Stock.product_id == Product.id)
        .filter(Stock.unit_id == unit_id)
        .all()
    )

    cardapio = []
    for produto, qtd in resultados:
        cardapio.append({
            "produto_id": produto.id,
            "nome": produto.name if hasattr(produto, 'name') else produto.nome,
            "descricao": produto.description if hasattr(produto, 'description') else produto.descricao,
            "preco": produto.price if hasattr(produto, 'price') else produto.price,
            "quantidade_em_estoque": qtd
        })

    return cardapio