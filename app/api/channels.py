from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.order_channel import OrderChannel
from app.models.models import Usuario, TipoUsuarioEnum
from app.schemas.order import OrderChannelCreate, OrderChannelResponse
from app.core.security import get_current_user, permit  # <--- Importa o controlo de perfis

router = APIRouter(prefix="/channels", tags=["Canais de Pedido (Multicanalidade)"])


@router.post("/", response_model=OrderChannelResponse, status_code=status.HTTP_201_CREATED)
def create_channel(
    channel_in: OrderChannelCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(permit(TipoUsuarioEnum.ADMIN))  # <--- Apenas Administradores podem criar canais
):
    existing = db.query(OrderChannel).filter(OrderChannel.channel_name == channel_in.channel_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Este canal de pedido já está registado.")

    db_channel = OrderChannel(
        channel_name=channel_in.channel_name,
        description=channel_in.description
    )
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel


@router.get("/", response_model=List[OrderChannelResponse])
def list_channels(db: Session = Depends(get_db)):
    # Mantém-se público para consulta dos canais de atendimento disponíveis
    channels = db.query(OrderChannel).all()
    return channels