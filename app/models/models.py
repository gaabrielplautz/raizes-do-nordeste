from datetime import datetime
import enum
from app.core.database import Base
from sqlalchemy import Column, DateTime, Enum as SQLEnum, Float, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class TipoUsuarioEnum(str, enum.Enum):
  ADMIN = "admin"
  OPERADOR = "operador"
  CLIENTE = "cliente"


class Usuario(Base):
  __tablename__ = "usuarios"

  id = Column(Integer, primary_key=True, index=True)
  nome = Column(String, nullable=False)
  email = Column(String, unique=True, index=True, nullable=False)
  senha_hash = Column(String, nullable=False)
  # Utiliza o SQLEnum para garantir validação correta ao nível da BD e do Pydantic/SQLAlchemy
  tipo = Column(
      SQLEnum(TipoUsuarioEnum), default=TipoUsuarioEnum.CLIENTE, nullable=False
  )
  criado_em = Column(DateTime, default=datetime.utcnow)


class Produto(Base):
  __tablename__ = "produtos"

  id = Column(Integer, primary_key=True, index=True)
  nome = Column(String, nullable=False)
  descricao = Column(String, nullable=True)
  preco = Column(Float, nullable=False)

  # Relação com o estoque
  estoque = relationship("Estoque", back_populates="produto", uselist=False)


class Estoque(Base):
  __tablename__ = "estoque"

  id = Column(Integer, primary_key=True, index=True)
  produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
  quantidade = Column(Integer, nullable=False, default=0)

  produto = relationship("Produto", back_populates="estoque")


class CanalPedidoEnum(str, enum.Enum):
  APP = "APP"
  TOTEM = "TOTEM"
  BALCAO = "BALCAO"
  PICKUP = "PICKUP"
  WEB = "WEB"

class Pedido(Base):
  __tablename__ = "pedidos"

  id = Column(Integer, primary_key=True, index=True)
  canal_pedido = Column(
      String, nullable=False
  )  # Guarda valores como APP, TOTEM, etc.
  unit_id = Column(Integer, nullable=False)
  status = Column(String, default="AGUARDANDO_PAGAMENTO", nullable=False)
  total_amount = Column(Float, nullable=False, default=0.0)
  created_at = Column(DateTime, default=datetime.utcnow)

  # Relação com os itens do pedido
  itens = relationship(
      "ItemPedido", back_populates="pedido", cascade="all, delete-orphan"
  )


class ItemPedido(Base):
  __tablename__ = "itens_pedido"

  id = Column(Integer, primary_key=True, index=True)
  pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
  product_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
  quantity = Column(Integer, nullable=False)
  unit_price = Column(Float, nullable=False)

  pedido = relationship("Pedido", back_populates="itens")
  produto = relationship("Produto")

class Fidelidade(Base):
    __tablename__ = "fidelidade"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    pontos = Column(Integer, default=0)
    consentimento_lgpd = Column(Boolean, default=True)

    usuario = relationship("Usuario", backref="fidelidade")