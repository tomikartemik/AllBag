from fastapi import APIRouter, Depends, HTTPException

from elements.product.DAL import ProductDAL
from elements.product.schemas import ShowProduct as ShowProductSchema, UpdateProductRequest as UpdateProductRequestSchema, \
    UpdatedProductResponse as UpdatedProductResponseSchema, DeleteProductResponse as DeleteProductResponseSchema

from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession
from settings import get_async_session

product_router = APIRouter()

async def _get_product_by_id(
        product_id: int,
        session
) -> Union[ShowProductSchema, None]:
    product_dal = ProductDAL(session)
    product = await product_dal.get_product_by_id(product_id)
    if product is not None:
        return ShowProductSchema(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            remaining_amount=product.remaining_amount,
            color=product.color,
            size=product.size,
            sex=product.sex
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found"
        )

async def _get_product_by_name(
    name: str,
    session
) -> Union[ShowProductSchema, None]:
    product_dal = ProductDAL(session)
    product = await product_dal.get_product_by_name(name)
    if product is not None:
        return ShowProductSchema(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            remaining_amount=product.remaining_amount,
            color=product.color,
            size=product.size,
            sex=product.sex
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Product with name {name} not found"
        )

async def _get_all_products(
        session
) -> Union[List[ShowProductSchema], None]:
    product_dal = ProductDAL(session)
    products = await product_dal.get_all_products()
    if products is not None:
        return [ShowProductSchema(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            remaining_amount=product.remaining_amount,
            color=product.color,
            size=product.size,
            sex=product.sex
        ) for product in products]
    else:
        raise HTTPException(
            status_code=404,
            detail="Products not found"
        )



async def _create_product(
        body: ShowProductSchema,
        session
) -> Union[ShowProductSchema, None]:
    product_dal = ProductDAL(session)
    product = await product_dal.create_product(
        name=body.name,
        description=body.description,
        price=body.price,
        remaining_amount=body.remaining_amount,
        color=body.color,
        size=body.size,
        sex=body.sex
    )
    return ShowProductSchema(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        remaining_amount=product.remaining_amount,
        color=product.color,
        size=product.size,
        sex=product.sex
    )

async def _delete_product(
        product_id: int,
        session
) -> Union[int, None]:
    product_dal = ProductDAL(session)
    deleted_product_id = await product_dal.delete_product(
        product_id=product_id
    )
    return deleted_product_id

async def _update_product(
        product_id: int,
        body: ShowProductSchema,
        session
) -> Union[int, None]:
    product_dal = ProductDAL(session)
    updated_product_id = await product_dal.update_product(
        product_id=product_id,
        name=body.name,
        description=body.description,
        price=body.price,
        remaining_amount=body.remaining_amount,
        color=body.color,
        size=body.size,
        sex=body.sex
    )
    return updated_product_id


@product_router.get("", response_model=ShowProductSchema)
async def get_product_by_id(
        product_id: int,
        db: AsyncSession = Depends(get_async_session)
    ) -> ShowProductSchema:
    product = await _get_product_by_id(product_id, db)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found"
        )
    return product

@product_router.get("/all", response_model=List[ShowProductSchema])
async def get_all_products(
        db: AsyncSession = Depends(get_async_session)
    ) -> List[ShowProductSchema]:
    products = await _get_all_products(db)
    if products is None:
        raise HTTPException(
            status_code=404,
            detail="Products not found"
        )


@product_router.post("", response_model=ShowProductSchema)
async def create_product(
        product: ShowProductSchema,
        db: AsyncSession = Depends(get_async_session)
    ) -> ShowProductSchema:
    try:
        return await _create_product(product, db)
    except Exception as err:
        raise HTTPException(
            status_code=503,
            detail=f"Database error, {err}"
        )

@product_router.delete("", response_model=DeleteProductResponseSchema)
async def delete_product(
        product_id: int,
        db: AsyncSession = Depends(get_async_session)
    ) -> int | None:
    try:
        return await _delete_product(product_id, db)
    except Exception as err:
        raise HTTPException(
            status_code=503,
            detail=f"Database error, {err}"
        )

@product_router.patch("", response_model=UpdatedProductResponseSchema)
async def update_product(
        product_id: int,
        body: UpdateProductRequestSchema,
        db: AsyncSession = Depends(get_async_session)
    ) -> int | None:
    try:
        return await _update_product(product_id, body, db)
    except Exception as err:
        raise HTTPException(
            status_code=503,
            detail=f"Database error, {err}"
        )