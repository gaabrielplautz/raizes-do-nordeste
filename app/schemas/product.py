from pydantic import BaseModel
from typing import Optional

# Schemas de Stock
class StockBase(BaseModel):
    quantity: int
    min_quantity: Optional[int] = 5

class StockCreate(StockBase):
    product_id: int

class StockResponse(StockBase):
    id: int
    product_id: int

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
    initial_stock: Optional[int] = 0  # Permite definir o stock inicial ao criar o produto

class ProductResponse(ProductBase):
    id: int
    stock: Optional[StockResponse] = None

    class Config:
        from_attributes = True