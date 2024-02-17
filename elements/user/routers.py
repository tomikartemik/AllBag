import uuid

from fastapi import APIRouter, Depends, HTTPException

from typing import List, Union

from elements.user.DAL import UserDAL
from elements.user.schemas import ShowUser as ShowUserSchema, UserCreate as UserCreateSchema, \
    DeleteUserResponse as DeleteUserResponseSchema, UpdatedUserResponse as UpdatedUserResponseSchema, \
    UpdateUserRequest as UpdateUserRequestSchema
from sqlalchemy.ext.asyncio import AsyncSession
from settings import get_async_session

user_router = APIRouter()

async def _get_user_by_id(
        user_id: uuid.UUID,
        session
) -> Union[ShowUserSchema, None]:
    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_id(user_id)
    if user is not None:
        return ShowUserSchema(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            number=user.number,
            email=user.email,
            is_active=user.is_active
        )

async def _create_user(
        body: UserCreateSchema,
        session
) -> Union[ShowUserSchema, None]:
    user_dal = UserDAL(session)
    user = await user_dal.create_user(
        name=body.name,
        surname=body.surname,
        number=body.number,
        email=body.email,
        is_active=body.is_active
    )
    return ShowUserSchema(
        user_id=user.user_id,
        name=user.name,
        surname=user.surname,
        number=user.number,
        email=user.email,
        is_active=user.is_active
    )

async def _delete_user(
        user_id: uuid.UUID,
        session
) -> Union[uuid.UUID, None]:
    user_dal = UserDAL(session)
    deleted_user_id = await user_dal.delete_user(
        user_id=user_id
    )
    return deleted_user_id

async def _update_user(
        user_id: uuid.UUID,
        body: UpdateUserRequestSchema,
        session
    ) -> Union[uuid.UUID, None]:
    user_dal = UserDAL(session)
    updated_user_id = await user_dal.update_user(
        user_id=user_id,
        name=body.name,
        surname=body.surname,
        number=body.number,
        email=body.email,
        is_active=body.is_active
    )
    return updated_user_id


@user_router.get("/{user_id}", response_model=ShowUserSchema)
async def get_user_by_id(
        user_id: uuid.UUID,
        db: AsyncSession = Depends(get_async_session)
    ) -> ShowUserSchema:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )
    return user

@user_router.post("", response_model=ShowUserSchema)
async def create_user(
        user: UserCreateSchema,
        db: AsyncSession = Depends(get_async_session)
    ) -> ShowUserSchema:
    try:
        return await _create_user(user, db)
    except Exception as err:
        raise HTTPException(
            status_code=503,
            detail=f"Database error, {err}"
        )
