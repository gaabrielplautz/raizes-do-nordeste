from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Pedido as Order, Usuario, Fidelidade
from app.core.security import get_current_user  # Importa a segurança JWT
from pydantic import BaseModel

router = APIRouter(prefix="/pagamentos", tags=["Pagamento Mock"])


class PaymentRequest(BaseModel):
    pedidoId: int
    valor: float
    gateway: str = "MOCK"
    simularRecusa: bool = False  # Se true, simula cartão recusado


@router.post("/", status_code=status.HTTP_200_OK)
def process_payment(
        payment: PaymentRequest,
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)  # Exige autenticação por Token JWT
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
    order.status = "PREPARACAO"  # Atualiza para cozinha/preparação

    # Atribuição automática de pontos de fidelidade (Regra RF06) após o pagamento aprovado
    # Utiliza o id do utilizador autenticado atual (current_user)
    fidelidade = db.query(Fidelidade).filter(Fidelidade.usuario_id == current_user.id).first()

    if not fidelidade:
        # Se o utilizador ainda não tiver registo, cria um automaticamente com consentimento ativo
        fidelidade = Fidelidade(usuario_id=current_user.id, pontos=0, consentimento_lgpd=True)
        db.add(fidelidade)
        db.commit()
        db.refresh(fidelidade)

    if fidelidade.consentimento_lgpd:
        # Regra: 1 ponto por unidade monetária gasta (convertido para inteiro)
        pontos_ganhos = int(payment.valor)
        fidelidade.pontos += pontos_ganhos

    db.commit()

    return {
        "statusTransacao": "APROVADO",
        "mensagem": "Pagamento processado com sucesso pelo gateway mock.",
        "pedidoId": order.id,
        "statusPedido": order.status,
        "valor": payment.valor
    }