from fastapi import APIRouter, Body, Depends
from app.api.dependencies.services.user import get_user_service
from app.dto.auth import AuthClaims
from app.dto.common import Pagination
from app.dto.user import (
    UserCreate,
    UserFilter,
    UserPasswordReset,
    UserPasswordUpdate,
    UserResponse,
    UserUpdate,
)
from app.services.user import UserService
from app.middlewares.main import middleware


# router
router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def get_users(
    filter: UserFilter = Depends(),
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    users, pagination = await user_service.get_users(filter)

    return {
        "users": [UserResponse.model_validate(user) for user in users],
        "pagination": Pagination.model_validate(pagination),
    }


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    user = await user_service.get_user_by_id(user_id=user_id)

    return {
        "user": UserResponse.model_validate(user),
    }


@router.post("")
async def create_user(
    data: UserCreate = Body(..., embed=True),
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    inserted_id = await user_service.create_user(data, auth_user)

    return {
        "message": "USER_CREATED_SUCCESSFULLY",
        "inserted_id": inserted_id,
    }


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    data: UserUpdate = Body(..., embed=True),
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    await user_service.update_user(user_id, data, auth_user)

    return {
        "message": "USER_UPDATED_SUCCESSFULLY",
    }


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    await user_service.delete_user(user_id, auth_user)

    return {
        "message": "USER_DELETED_SUCCESSFULLY",
    }


@router.put("/password/{user_id}")
async def update_password(
    user_id: str,
    data: UserPasswordUpdate = Body(..., embed=True),
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    await user_service.update_password(user_id, data, auth_user)

    return {
        "message": "USER_PASSWORD_UPDATED_SUCCESSFULLY",
    }


@router.put("/password/reset/{user_id}")
async def reset_password(
    user_id: str,
    data: UserPasswordReset = Body(..., embed=True),
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    await user_service.reset_password(user_id, data, auth_user)

    return {
        "message": "USER_PASSWORD_RESET_SUCCESSFULLY",
    }
