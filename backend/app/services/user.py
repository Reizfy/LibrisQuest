from typing import Optional
from app.core.exception import (
    DataNotFoundException,
    ForbiddenException,
    InternalServerException,
    InvalidOldPasswordException,
    PayloadRequiredException,
    UsernameExistException,
)
from app.dto.auth import AuthClaims
from app.dto.common import Pagination
from app.dto.user import (
    UserCreate,
    UserFilter,
    UserPasswordReset,
    UserPasswordUpdate,
    UserUpdate,
)
from app.enums.user import UserRoleEnum
from app.models.user import User
from app.repositories.user import AbstractUserRepository
from app.utils.common import get_current_datetime
from app.utils.password import generate_hashed_password, verify_hash_password


class UserService:
    def __init__(self, user_repo: AbstractUserRepository):
        self.user_repo = user_repo

    async def get_users(self, filter: UserFilter) -> tuple[list[User], Pagination]:
        users, total = await self.user_repo.find_all(filter)
        pagination = Pagination(
            page=filter.page,
            items=filter.items,
            total=total,
        )

        return users, pagination

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        # check existing user
        user = await self.user_repo.find_by_id(user_id)
        if not user:
            raise DataNotFoundException()

        return user

    async def create_user(self, data: UserCreate, auth_user: AuthClaims) -> str:
        # protect access
        if auth_user.role != UserRoleEnum.ADMIN.value:
            raise ForbiddenException()

        # check duplicated user
        if await self.user_repo.find_by_username(data.username):
            raise UsernameExistException()

        # formatting user data
        new_user = User(
            **data.model_dump(exclude={"password"}),
            password=generate_hashed_password(data.password),
            created_at=get_current_datetime(),
            created_by=auth_user.id,
        )

        # creating user
        inserted_id = await self.user_repo.create(new_user)
        if not inserted_id:
            raise InternalServerException()

        return inserted_id

    async def update_user(
        self, user_id: str, data: UserUpdate, auth_user: AuthClaims
    ) -> bool:
        # check existing user
        exist_user = await self.user_repo.find_by_id(user_id)
        if not exist_user:
            raise DataNotFoundException()

        # protect access
        if auth_user.role != UserRoleEnum.ADMIN.value and exist_user.id != auth_user.id:
            raise ForbiddenException()

        # check duplicated user
        if data.username != exist_user.username:
            duplicated_user = await self.user_repo.find_by_username(data.username)
            if duplicated_user:
                raise UsernameExistException()

        # formatting update data
        update_payload = data.model_dump(exclude_unset=True)
        if not update_payload:
            raise PayloadRequiredException()

        update_payload["updated_at"] = get_current_datetime()
        update_payload["updated_by"] = auth_user.id

        # updating user
        if not await self.user_repo.update_by_id(user_id, update_payload):
            raise InternalServerException()

        return True

    async def delete_user(self, user_id: str, auth_user: AuthClaims) -> bool:
        # protect access
        if auth_user.role != UserRoleEnum.ADMIN.value:
            raise ForbiddenException()

        # check existing user
        if not await self.user_repo.find_by_id(user_id):
            raise DataNotFoundException()

        # deleting user
        if not await self.user_repo.delete_by_id(user_id):
            raise InternalServerException()

        return True

    async def update_password(
        self, user_id: str, data: UserPasswordUpdate, auth_user: AuthClaims
    ) -> bool:
        # check existing user
        exist_user = await self.user_repo.find_by_id(user_id)
        if not exist_user:
            raise DataNotFoundException()

        # verify old password
        if not verify_hash_password(data.current_password, exist_user.password):
            raise InvalidOldPasswordException()

        # formatting update data
        update_payload = {
            "password": generate_hashed_password(data.new_password),
            "updated_password_at": get_current_datetime(),
            "updated_password_by": auth_user.id,
        }

        # updating password
        if not await self.user_repo.update_by_id(user_id, update_payload):
            raise InternalServerException()

        return True

    async def reset_password(
        self, user_id: str, data: UserPasswordReset, auth_user: AuthClaims
    ) -> bool:
        # protect access
        if auth_user.role != UserRoleEnum.ADMIN.value:
            raise ForbiddenException()

        # check existing user
        if not await self.user_repo.find_by_id(user_id):
            raise DataNotFoundException()

        # formatting update data
        update_payload = {
            "password": generate_hashed_password(data.new_password),
            "updated_password_at": get_current_datetime(),
            "updated_password_by": auth_user.id,
        }

        # updating password
        if not await self.user_repo.update_by_id(user_id, update_payload):
            raise InternalServerException()

        return True
