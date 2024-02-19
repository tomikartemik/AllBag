from typing import List

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "order"
    id: int = Column("id", Integer, primary_key=True)
    created_at: DateTime = Column("created_at", DateTime, nullable=False)
    status: String = Column("status", String)

    # products_id: List[int] = Column("products_id", Integer, ForeignKey("product."))