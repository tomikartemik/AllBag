from typing import Optional
import re
import uuid
from fastapi import HTTPException
from pydantic import BaseModel, constr
from pydantic import EmailStr
from pydantic import validator


class ShowProduct(BaseModel):
    id: int
    name: str
    description: str
    price: float
    remaining_amount: int
    color: str
    size: str
    sex: str
    category: int
    brand: int
    # TODO: нужны все поля
    # photo_link: str


class AddProduct(BaseModel):
    name: str
    description: str
    price: float
    remaining_amount: int
    color: str
    size: str
    sex: str
    # category_id: int
    # photo_link: str


class DeleteProductResponse(BaseModel):
    deleted_product_id: int


class UpdatedProductResponse(BaseModel):
    updated_product_id: int


class UpdateProductRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    description: Optional[constr(min_length=1)]
    price: Optional[float]
    remaining_amount: Optional[int]
    color: Optional[str]
    size: Optional[str]
    sex: Optional[str]
    # category_id: Optional[int] = Field(None)
    # photo_link: Optional[str] = Field(None)
