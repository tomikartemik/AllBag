from typing import Union, List

from sqlalchemy import update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from elements.product.models import Product as ProductModel


class ProductDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_product(
            self,
            name: str,
            description: str,
            price: float,
            remaining_amount: int,
            color: str = None,
            size: str = None,
            sex: str = None,
            # category_id: UUID = None,
            # photo_link: str = None
    ) -> ProductModel:
        new_product = ProductModel(
            name=name,
            description=description,
            price=price,
            remaining_amount=remaining_amount,
            color=color,
            size=size,
            sex=sex
        )
        self.db_session.add(new_product)
        await self.db_session.flush()
        return new_product

    async def delete_product(self, product_id: int) -> Union[int, None]:
        query = update(ProductModel). \
            where(and_(ProductModel.id == product_id, ProductModel.is_active == True)). \
            values(is_working=False).returning(ProductModel.id)
        res = await self.db_session.execute(query)
        deleted_product_id_row = res.fetchone()
        if deleted_product_id_row is not None:
            return deleted_product_id_row[0]

    async def get_product_by_id(self, product_id: int) -> Union[ProductModel, None]:
        query = select(ProductModel).where(ProductModel.id == product_id)
        res = await self.db_session.execute(query)
        product = res.fetchone()
        if product is not None:
            return product[0]

    async def get_all_products(
            self,
            limit: int,
            offset: int,
            category: int | None = None,
            color: int | None = None,
            brand: int | None = None,
            price: (int, int) | None = None
    ) -> List[ProductModel]:
        query = select(ProductModel)
        if category is not None:
            query = query.where(ProductModel.category_id == category)
        if color is not None:
            query = query.where(ProductModel.color == color)
        if brand is not None:
            query = query.where(ProductModel.brand_id == brand)
        if price is not None:
            query = query.where(and_(ProductModel.price >= price[0], ProductModel.price <= price[1]))
        query = query.offset(offset).limit(limit)

        res = await self.db_session.execute(query)
        products = res.fetchall()
        if products is not None:
            return [product[0] for product in products]

    async def update_product(self, product_id: int, **kwargs) -> Union[int, None]:
        query = update(ProductModel).where(ProductModel.id == product_id).values(kwargs).returning(ProductModel.id)
        res = await self.db_session.execute(query)
        updated_product_id_row = res.fetchone()
        if updated_product_id_row is not None:
            return updated_product_id_row[0]
