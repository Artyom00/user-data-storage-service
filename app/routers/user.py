from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils import edit_user, paginate_items
from app.db.database import get_db
from app.db.models import User
from app.schemas import CurrentUserResponseModel, UpdateUserModel, \
    UpdateUserResponseModel, UsersListResponseModel
from app.services.user import get_current_user

router = APIRouter(prefix='/users', tags=['user'])


@router.get('/current', response_model=CurrentUserResponseModel)
async def get_logged_in_user(user: User = Depends(get_current_user)):
    return user


@router.patch('/{pk}', response_model=UpdateUserResponseModel)
async def edit_current_user(pk: int, request: UpdateUserModel,
                            db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    return await edit_user(pk, request, db, current_user)


@router.get('', response_model=Page[UsersListResponseModel])
async def paginate_users(current_user=Depends(get_current_user),
                         params: Params = Depends(),
                         db: AsyncSession = Depends(get_db)):
    return await paginate_items(current_user, params, db)
