from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from elements.category.models import Category

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    id: int = Column("id", Integer, primary_key=True)
    name: str = Column("name", String, nullable=False)
    description: str = Column("description", String, nullable=False)
    price: float = Column("price", Float, nullable=False)
    remaining_amount: int = Column("remaining_amount", Integer, nullable=False)
    color: str = Column("color", String, nullable=True)
    size: str = Column("size", String, nullable=True)
    sex: str = Column("sex", String, nullable=True)
    category_id: int = Column("category_id", Integer, ForeignKey(Category.id), nullable=False)

    # TODO: photo_link
    # photo_link: str = Column("photo_link", String, nullable=False)
