from typing import Union
from uuid import UUID

from sqlalchemy import update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from elements.user.models import User as UserModel

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class UserDAL:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self,
            name: str,
            surname: str,
            number: str,
            email: str,
            is_active: bool = True
    ) -> UserModel:
        new_user = UserModel(
            name=name,
            surname=surname,
            number=number,
            email=email,
            is_active=is_active

        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = update(UserModel).\
            where(and_(UserModel.user_id == user_id, UserModel.is_active == True)).\
            values(is_working=False).returning(UserModel.user_id)
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[UserModel, None]:
        query = select(UserModel).where(UserModel.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = update(UserModel). \
            where(and_(UserModel.user_id == user_id, UserModel.is_active == True)). \
            values(kwargs). \
            returning(UserModel.user_id)
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]