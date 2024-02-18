from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import declarative_base

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

    # TODO: add category_id and photo_link

    # category_id: int = Column("category_id", Integer, ForeignKey("category.id"), nullable=False)
    # photo_link: str = Column("photo_link", String, nullable=False)
