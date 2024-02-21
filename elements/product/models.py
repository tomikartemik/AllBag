from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from elements.category.models import Category
from elements.order.models import association_table, Order as OrderModel

Base = declarative_base()


class Brand(Base):
    __tablename__ = 'brand'

    id: int = Column("id", Integer, primary_key=True)
    name: str = Column("name", String, nullable=False)


class Product(Base):
    __tablename__ = "product"

    id: int = Column("id", Integer, primary_key=True)
    name: str = Column("name", String, nullable=False)
    description: str = Column("description", String, nullable=False)
    price: float = Column("price", Float, nullable=False)
    remaining_amount: int = Column("remaining_amount", Integer, nullable=False)
    brand_id: int = Column("brand_id", Integer, ForeignKey(Brand.Id))
    color: str = Column("color", String, nullable=True)
    size: str = Column("size", String, nullable=True)
    sex: str = Column("sex", String, nullable=True)
    category_id: int = Column("category_id", Integer, ForeignKey(Category.id, ondelete="CASCADE"), nullable=False)

    orders = relationship(
        OrderModel,
        secondary=association_table,
        back_populates="products"
    )


class Photo(Base):
    __tablename__ = "photo"

    id: int = Column("id", Integer, primary_key=True)
    url: str = Column("url", String, nullable=False)
    product_id: int = Column("product_id", Integer, ForeignKey(Product.id), nullable=False)
