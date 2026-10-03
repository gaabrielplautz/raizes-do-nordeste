from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Fidelidade, Usuario
from app.schemas.fidelidade import FidelidadeResponse, ResgatePontosRequest
from app.core.security import get_current_user

router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])


@router.get("/", response_model=FidelidadeResponse)
def consultar_fidelidade(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    """Consulta os pontos de fidelidade do usuário logado."""
    fidelidade = db.query(Fidelidade).filter(Fidelidade.usuario_id == current_user.id).first()

    if not fidelidade:
        # Se não existir registo, cria automaticamente com 0 pontos e LGPD ativa para o usuário
        fidelidade = Fidelidade(usuario_id=current_user.id, pontos=0, consentimento_lgpd=True)
        db.add(fidelidade)
        db.commit()
        db.refresh(fidelidade)

    return fidelidade


@router.post("/resgatar", response_model=FidelidadeResponse)
def resgatar_pontos(
    payload: ResgatePontosRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Permite ao usuário resgatar pontos do programa de fidelidade."""
    fidelidade = db.query(Fidelidade).filter(Fidelidade.usuario_id == current_user.id).first()

    if not fidelidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registo de fidelidade não encontrado."
        )

    #Valida se o utilizador possui consentimento ativo para movimentar pontos
    if not fidelidade.consentimento_lgpd:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resgate não permitido: consentimento LGPD inativo."
        )

    # Valida se possui saldo suficiente
    if fidelidade.pontos < payload.quantidade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo de pontos insuficiente para o resgate."
        )

    fidelidade.pontos -= payload.quantidade
    db.commit()
    db.refresh(fidelidade)

    return fidelidade