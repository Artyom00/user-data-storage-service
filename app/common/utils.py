from typing import Union

from fastapi import status
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import User
from app.exceptions import ErrorResponse
from app.schemas import UpdateUserModel, PrivateUpdateUserModel


async def edit_user(pk: int,
                    request: Union[UpdateUserModel, PrivateUpdateUserModel],
                    db: AsyncSession, current_user: User):
    user = await db.get(User, pk)

    if not user:
        raise ErrorResponse('User not found', status.HTTP_404_NOT_FOUND)

    if not current_user.is_admin:
        if current_user.id != pk:
            raise ErrorResponse(
                'You can only change your personal data',
                status.HTTP_403_FORBIDDEN)

    await db.execute(update(User).where(User.id == pk).values(
        request.dict(exclude_unset=True)))
    await db.commit()

    return await db.get(User, pk)


async def paginate_items(user: User, params: Params, db: AsyncSession):
    if user.is_admin:
        query = select(User).where(User.id != user.id).options(
            selectinload(User.city_ref))

    else:
        query = select(User).where(User.id != user.id)

    return await paginate(db, query, params)
