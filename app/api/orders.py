from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product, Stock
from app.models.models import Pedido as Order, ItemPedido as OrderItem
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter(prefix="/pedidos", tags=["Pedidos e Fluxo Crítico"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # 1. Validar e calcular itens do pedido
    total_amount = 0.0
    validated_items = []

    for item in order_data.itens:
        product = db.query(Product).filter(Product.id == item.produtoId).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {item.produtoId} não encontrado."
            )

        # Verificar stock na unidade
        stock = db.query(Stock).filter(
            Stock.product_id == item.produtoId,
            Stock.unit_id == order_data.unidadeId
        ).first()

        if not stock or stock.quantity < item.quantidade:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "ESTOQUE_INSUFICIENTE",
                    "message": f"Quantidade indisponível para o produto '{product.name}'.",
                    "details": [{"field": f"itens.produtoId_{item.produtoId}",
                                 "issue": f"Disponível: {stock.quantity if stock else 0}"}]
                }
            )

        subtotal = float(product.price) * item.quantidade
        total_amount += subtotal
        validated_items.append((product, item.quantidade, float(product.price)))

    # 2. Criar o Pedido registrando o canalPedido obrigatório
    new_order = Order(
        canal_pedido=order_data.canalPedido,
        unit_id=order_data.unidadeId,
        status="AGUARDANDO_PAGAMENTO",
        total_amount=total_amount
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # 3. Dar baixa no stock e associar os itens
    for product, qty, price in validated_items:
        stock = db.query(Stock).filter(
            Stock.product_id == product.id,
            Stock.unit_id == order_data.unidadeId
        ).first()
        stock.quantity -= qty

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=qty,
            unit_price=price
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)
    return new_order