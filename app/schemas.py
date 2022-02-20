import datetime

from pydantic import BaseModel


class PrivateCreateUserModel(BaseModel):
    first_name: str
    last_name: str | None
    other_name: str | None
    email: str
    phone: str | None
    birthday: datetime.date | None
    city: int | None
    additional_info: str | None
    is_admin: bool
    password: str

    class Config:
        extra = 'forbid'


class PrivateDetailUserResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    other_name: str | None
    email: str
    phone: str | None
    birthday: datetime.date | None
    city: int | None
    additional_info: str | None
    is_admin: bool

    class Config:
        orm_mode = True


class PrivateUpdateUserModel(BaseModel):
    id: int | None
    first_name: str | None
    last_name: str | None
    other_name: str | None
    email: str | None
    phone: str | None
    birthday: datetime.date | None
    city: int | None
    additional_info: str | None
    is_admin: bool | None

    class Config:
        extra = 'forbid'


class CitiesHintModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UsersListResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    email: str

    class Config:
        orm_mode = True


class PrivateUsersListResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    email: str
    city_ref: CitiesHintModel | None

    class Config:
        orm_mode = True


class LoginModel(BaseModel):
    login: str
    password: str

    class Config:
        extra = 'forbid'


class CurrentUserResponseModel(BaseModel):
    first_name: str
    last_name: str | None
    other_name: str | None
    email: str
    phone: str | None
    birthday: datetime.date | None
    is_admin: bool

    class Config:
        orm_mode = True


class UpdateUserResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    other_name: str | None
    email: str
    phone: str | None
    birthday: datetime.date | None

    class Config:
        orm_mode = True


class UpdateUserModel(BaseModel):
    first_name: str | None
    last_name: str | None
    other_name: str | None
    email: str | None
    phone: str | None
    birthday: datetime.date | None

    class Config:
        extra = 'forbid'
