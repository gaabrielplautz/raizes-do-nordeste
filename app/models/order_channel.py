from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from app.core.database import Base

class OrderChannel(Base):
    __tablename__ = "order_channels"

    id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String, unique=True, nullable=False)  # Ex: WhatsApp, Loja Fisica, App
    description = Column(String, nullable=True)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    channel_id = Column(Integer, ForeignKey("order_channels.id"), nullable=False)
    status = Column(String, default="PENDENTE", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)