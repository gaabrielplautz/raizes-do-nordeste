from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Pedido as Order, Usuario
from app.core.security import get_current_user  # <--- Importa a segurança JWT
from pydantic import BaseModel

router = APIRouter(prefix="/pagamentos", tags=["Pagamento Mock"])

class PaymentRequest(BaseModel):
    pedidoId: int
    valor: float
    gateway: str = "MOCK"
    simularRecusa: bool = False # Se true, simula cartão recusado

@router.post("/", status_code=status.HTTP_200_OK)
def process_payment(
    payment: PaymentRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)  # <--- Exige autenticação por Token JWT
):
    order = db.query(Order).filter(Order.id == payment.pedidoId).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado."
        )

    if payment.simularRecusa:
        order.status = "PAGAMENTO_RECUSADO"
        db.commit()
        return {
            "statusTransacao": "RECUSADO",
            "mensagem": "Transação negada pela instituição financeira simulada.",
            "pedidoId": order.id,
            "statusPedido": order.status
        }

    # Pagamento Aprovado com sucesso
    order.status = "PREPARACAO" # Atualiza para cozinha/preparação
    db.commit()

    return {
        "statusTransacao": "APROVADO",
        "mensagem": "Pagamento processado com sucesso pelo gateway mock.",
        "pedidoId": order.id,
        "statusPedido": order.status,
        "valor": payment.valor
    }