from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Schemas de Canal de Pedido
class OrderChannelBase(BaseModel):
    channel_name: str
    description: Optional[str] = None

class OrderChannelCreate(OrderChannelBase):
    pass

class OrderChannelResponse(OrderChannelBase):
    id: int

    class Config:
        from_attributes = True

# Schema para os itens individuais do pedido
class OrderItemCreate(BaseModel):
    produtoId: int
    quantidade: int

class OrderItemResponse(BaseModel):
    id: int
    produtoId: int = Field(..., validation_alias="product_id")
    quantidade: int = Field(..., validation_alias="quantity")
    unit_price: float

    class Config:
        from_attributes = True
        populate_by_name = True

# Schemas de Pedidos
class OrderBase(BaseModel):
    canal_pedido: str
    unit_id: int
    status: Optional[str] = "AGUARDANDO_PAGAMENTO"
    total_amount: Optional[float] = 0.0

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    itens: List[OrderItemResponse] = []

    class Config:
        from_attributes = True