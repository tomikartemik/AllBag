from sqlalchemy import Column, Boolean, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: String = Column(String, nullable=False)
    surname: String = Column(String, nullable=False)
    number: String = Column(String, nullable=False, unique=True)
    email: String = Column(String, nullable=False, unique=True)

    orders = relationship("Order", back_populates="user")
