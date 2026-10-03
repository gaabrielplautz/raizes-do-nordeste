from pydantic import BaseModel
from typing import Optional

# Schemas de Stock
class StockBase(BaseModel):
    quantity: int
    min_quantity: Optional[int] = 5
    unit_id: int  # <--- Adicionado para suportar o stock por unidade

class StockCreate(StockBase):
    product_id: int

class StockResponse(StockBase):
    id: int
    product_id: int
    unit_id: int  # <--- Incluído na resposta

    class Config:
        from_attributes = True

# Schemas de Produto
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    is_active: Optional[bool] = True

class ProductCreate(ProductBase):
    initial_stock: Optional[int] = 0
    unit_id: int  # <--- Recebe a unidade onde o produto será cadastrado

class ProductResponse(ProductBase):
    id: int
    stock: Optional[StockResponse] = None

    class Config:
        from_attributes = True