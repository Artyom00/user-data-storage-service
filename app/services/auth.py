from fastapi import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.hashing import Hash
from app.db.models import User
from app.exceptions import BadRequestResponse
from app.schemas import LoginModel


async def verify_user(credentials: LoginModel, db: AsyncSession,
                      response: Response):
    user = await db.scalar(
        select(User).where(User.email == credentials.login))

    if not user:
        raise BadRequestResponse('Incorrect login')

    if not Hash.verify(user.password, credentials.password):
        raise BadRequestResponse('Incorrect password')

    response.set_cookie(key='user_id', value=user.id)

    return user


def sign_out(response: Response):
    response.delete_cookie(key='user_id')
    return 'Logout completed successfully'
