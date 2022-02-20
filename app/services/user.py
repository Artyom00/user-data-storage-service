from fastapi import Request, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.exceptions import ErrorResponse


async def get_current_user(request: Request,
                           db: AsyncSession = Depends(get_db)):
    id_ = request.cookies.get('user_id')

    if not id_:
        raise ErrorResponse('Unauthorized',
                            status.HTTP_401_UNAUTHORIZED)
    return await db.scalar(select(User).where(User.id == int(id_)))


async def is_admin(request: Request,
                   current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise ErrorResponse('Access denied', status.HTTP_403_FORBIDDEN)
    return current_user
