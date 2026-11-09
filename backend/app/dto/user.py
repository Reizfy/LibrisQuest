from datetime import datetime
from typing import Optional
from app.dto.common import BaseRequestModel, BaseResponseModel
from app.enums.common import SortOrderEnum
from app.enums.user import UserRoleEnum, UserSortByEnum


# --- requests ---
class UserFilter(BaseRequestModel):
    role: Optional[UserRoleEnum] = None
    key: Optional[str] = None
    page: int = 1
    items: int = 10
    sort_by: UserSortByEnum = UserSortByEnum.CREATED_AT.value
    sort_order: SortOrderEnum = SortOrderEnum.DESC.value


class UserCreate(BaseRequestModel):
    name: str
    username: str
    password: str
    role: UserRoleEnum
    is_active: bool = True
    email: Optional[str] = None
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None


class UserUpdate(BaseRequestModel):
    name: Optional[str] = None
    username: Optional[str] = None
    role: Optional[UserRoleEnum] = None
    is_active: Optional[bool] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None


class UserPasswordUpdate(BaseRequestModel):
    current_password: str
    new_password: str


class UserPasswordReset(BaseRequestModel):
    new_password: str


# --- responses ---
class UserResponse(BaseResponseModel):
    id: str
    name: str
    username: str
    role: int
    is_active: bool = False
    email: Optional[str] = None
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None
    created_at: Optional[datetime] = None
