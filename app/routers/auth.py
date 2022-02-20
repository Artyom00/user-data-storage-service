from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas import LoginModel, CurrentUserResponseModel
from app.services.auth import verify_user, sign_out

router = APIRouter(prefix='', tags=['auth'])


@router.post('/login', response_model=CurrentUserResponseModel)
async def login(credentials: LoginModel, response: Response,
                db: AsyncSession = Depends(get_db)):
    return await verify_user(credentials, db, response)


@router.get('/logout')
async def logout(response: Response):
    return sign_out(response)
