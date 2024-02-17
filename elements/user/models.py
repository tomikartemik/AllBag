from sqlalchemy import Column, Boolean, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    number = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), nullable=False)

    orders = relationship("Order", back_populates="user")
