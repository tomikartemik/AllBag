from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from sqlalchemy import Column, Boolean, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import settings
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator

##############################################
# BLOCK FOR COMMON INTERACTION WITH DATABASE #
##############################################


# create async engine for interaction with database
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

# create session for the interaction with database
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

##############################
# BLOCK WITH DATABASE MODELS #
##############################


Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=False)
    category = Column(String, nullable=False)
    remain = Column(Integer, nullable=False)
    size = Column(Integer, nullable=True)
    color = Column(String, nullable=True)
    sex = Column(String, nullable=True)


class Order(Base):
    __tablename__ = "orders"
    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False)

    products = relationship("Product", back_populates="order")

    user_id = Column(UUID, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="orders")


###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


#########################
# BLOCK WITH API MODELS #
#########################

#########################
# BLOCK WITH API ROUTES #
#########################

# create instance of the app
app = FastAPI(title="luchanos-oxford-university")

user_router = APIRouter()


async def _create_new_user(body: UserCreate) -> ShowUser:
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)


# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
