from fastapi import APIRouter, status, Response, Depends
from fastapi_pagination import Params, Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils import edit_user, paginate_items
from app.db.database import get_db
from app.db.models import User
from app.schemas import PrivateDetailUserResponseModel, PrivateCreateUserModel, \
    PrivateUsersListResponseModel, PrivateUpdateUserModel
from app.services.admin import add_user, get_user, remove_user
from app.services.user import is_admin

router = APIRouter(prefix='/private', tags=['admin'])


@router.post('/users', response_model=PrivateDetailUserResponseModel,
             status_code=status.HTTP_201_CREATED)
async def create_user(request: PrivateCreateUserModel,
                      db: AsyncSession = Depends(get_db),
                      admin: User = Depends(is_admin)):
    return await add_user(request, db)


@router.get('/users/{pk}', response_model=PrivateDetailUserResponseModel)
async def get_user_info(pk: int, db: AsyncSession = Depends(get_db),
                        admin: User = Depends(is_admin)):
    return await get_user(pk, db)


@router.get('/users', response_model=Page[PrivateUsersListResponseModel])
async def paginate_users(admin: User = Depends(is_admin),
                         params: Params = Depends(),
                         db: AsyncSession = Depends(get_db)):
    return await paginate_items(admin, params, db)


@router.delete('/users/{pk}', status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response)
async def delete_user(pk: int, admin: User = Depends(is_admin),
                      db: AsyncSession = Depends(get_db)):
    await remove_user(pk, db, admin)


@router.patch('/users/{pk}', response_model=PrivateDetailUserResponseModel)
async def edit_user_info(request: PrivateUpdateUserModel, pk: int,
                         admin: User = Depends(is_admin),
                         db: AsyncSession = Depends(get_db)):
    return await edit_user(pk, request, db, admin)
