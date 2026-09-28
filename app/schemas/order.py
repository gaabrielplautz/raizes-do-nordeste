from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schemas de Canal de Pedido (canalPedido)
class OrderChannelBase(BaseModel):
    channel_name: str
    description: Optional[str] = None

class OrderChannelCreate(OrderChannelBase):
    pass

class OrderChannelResponse(OrderChannelBase):
    id: int

    class Config:
        from_attributes = True

# Schemas de Pedidos
class OrderBase(BaseModel):
    client_name: str
    total_amount: float
    channel_id: int
    status: Optional[str] = "PENDENTE"

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    channel: OrderChannelResponse

    class Config:
        from_attributes = True