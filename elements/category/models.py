from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = "category"
    id: int = Column("id", Integer, primary_key=True)
    name: str = Column("name", String, nullable=False)
