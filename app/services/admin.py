from fastapi import status
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.hashing import Hash
from app.db.models import User
from app.exceptions import ErrorResponse, BadRequestResponse
from app.schemas import PrivateCreateUserModel


async def add_user(request: PrivateCreateUserModel, db: AsyncSession):
    params = request.copy(update={
        'password': Hash.encrypt(request.password)
    })

    new_user = await db.execute(insert(User).values(**params.dict()))
    await db.commit()

    return {**request.dict(), 'id': new_user.inserted_primary_key[0]}


async def get_user(pk: int, db: AsyncSession):
    user = await db.get(User, pk)

    if not user:
        raise ErrorResponse('User not found', status.HTTP_404_NOT_FOUND)

    return user


async def remove_user(pk: int, db: AsyncSession, user: User):
    user = await db.get(User, pk)

    if not user:
        raise ErrorResponse('User not found', status.HTTP_404_NOT_FOUND)

    if user.id == pk:
        raise BadRequestResponse("Admin shouldn't delete own personal data")

    await db.execute(delete(User).where(User.id == pk))
    await db.commit()
