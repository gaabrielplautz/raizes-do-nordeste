from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.product import Product, Stock
from app.models.models import Usuario, TipoUsuarioEnum
from app.schemas.product import ProductCreate, ProductResponse, StockResponse, StockBase
from app.core.security import get_current_user, permit

router = APIRouter(prefix="/products", tags=["Produtos e Stock"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(permit(TipoUsuarioEnum.ADMIN, TipoUsuarioEnum.OPERADOR))
):
    # Verificar se já existe um produto com o mesmo nome
    existing = db.query(Product).filter(Product.name == product_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Produto já registado.")

    # Criar o produto
    db_product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        category=product_in.category,
        is_active=product_in.is_active
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Criar o stock inicial associado estritamente à unidade informada (RF04)
    db_stock = Stock(
        product_id=db_product.id,
        unit_id=product_in.unit_id,  # <--- Essencial para vincular o stock à unidade!
        quantity=product_in.initial_stock,
        min_quantity=5
    )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)

    return db_product


@router.get("/", response_model=List[ProductResponse])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@router.put("/{product_id}/stock", response_model=StockResponse)
def update_stock(
    product_id: int,
    stock_in: StockBase,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(permit(TipoUsuarioEnum.ADMIN, TipoUsuarioEnum.OPERADOR))
):
    stock = db.query(Stock).filter(Stock.product_id == product_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Registo de stock não encontrado para este produto.")

    stock.quantity = stock_in.quantity
    stock.min_quantity = stock_in.min_quantity
    db.commit()
    db.refresh(stock)
    return stock