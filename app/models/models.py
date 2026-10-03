from datetime import datetime
import enum
from app.core.database import Base
from sqlalchemy import Column, DateTime, Enum as SQLEnum, Float, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class TipoUsuarioEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    OPERADOR = "OPERADOR"
    CLIENTE = "CLIENTE"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            value_upper = value.upper()
            for member in cls:
                if member.value == value_upper:
                    return member
        return super()._missing_(value)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    tipo = Column(
        SQLEnum(
            TipoUsuarioEnum,
            native_enum=False,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        default=TipoUsuarioEnum.CLIENTE,
        nullable=False
    )
    criado_em = Column(DateTime, default=datetime.utcnow)


class Unidade(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    endereco = Column(String, nullable=True)
    ativa = Column(Boolean, default=True)

    # Relação com o estoque da unidade
    estoques = relationship("Estoque", back_populates="unidade", cascade="all, delete-orphan")
    pedidos = relationship("Pedido", back_populates="unidade")


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Float, nullable=False)

    # Um produto pode ter estoques em várias unidades
    estoques = relationship("Estoque", back_populates="produto", cascade="all, delete-orphan")


class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)  # RF02 e RF04: Estoque por Unidade
    quantidade = Column(Integer, nullable=False, default=0)

    produto = relationship("Produto", back_populates="estoques")
    unidade = relationship("Unidade", back_populates="estoques")


class CanalPedidoEnum(str, enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            value_upper = value.upper()
            for member in cls:
                if member.value == value_upper:
                    return member
        return super()._missing_(value)


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    canal_pedido = Column(String, nullable=False)
    unit_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)  # Vinculado à tabela Unidade
    status = Column(String, default="AGUARDANDO_PAGAMENTO", nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    unidade = relationship("Unidade", back_populates="pedidos")
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