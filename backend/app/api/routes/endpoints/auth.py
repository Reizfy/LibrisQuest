from fastapi import APIRouter, Body, Depends, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.core.limiter import limiter
from app.api.dependencies.services.auth import get_auth_service
from app.dto.auth import AuthLoginResponse, AuthRefreshToken, AuthRefreshTokenResponse
from app.dto.common import RequestContext
from app.services.auth import AuthService


# router
router = APIRouter(prefix="/auth", tags=["Authentications"])


@router.post("/login", response_model=AuthLoginResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    data: OAuth2PasswordRequestForm = Depends(),
    is_remember: bool = Form(False),
    auth_service: AuthService = Depends(get_auth_service),
):
    context = RequestContext(
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("User-Agent"),
    )
    access_token, refresh_token, user = await auth_service.login(
        context=context,
        username=data.username,
        password=data.password,
        is_remember=is_remember,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user,
    }


@router.post("/refresh-token", response_model=AuthRefreshTokenResponse)
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    data: AuthRefreshToken = Body(..., embed=True),
    auth_service: AuthService = Depends(get_auth_service),
):
    access_token, refresh_token = await auth_service.refresh_token(
        refresh_token=data.refresh_token
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
