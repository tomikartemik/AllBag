from typing import List

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from elements.product.models import Product as ProductModel

Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('order_id', Integer, ForeignKey(Order.id, ondelete="CASCADE")),
                          Column('product_id', Integer, ForeignKey(ProductModel.id, ondelete="CASCADE"))
                          )


class Order(Base):
    __tablename__ = "order"
    id: int = Column("id", Integer, primary_key=True)
    created_at: DateTime = Column("created_at", DateTime, nullable=False)
    status: str = Column("status", String)
    payment_method: str = Column("payment_method", String, nullable=False)

    products = relationship(
        ProductModel,
        secondary=association_table,
        back_populates="orders"
    )

    # products_id: List[int] = Column("products_id", Integer, ForeignKey("product."))
