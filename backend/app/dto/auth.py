from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.dto.common import BaseRequestModel, BaseResponseModel
from app.enums.common import TokenTypeEnum


# --- requests ---
class AuthRefreshToken(BaseRequestModel):
    refresh_token: str


class AuthClaims(BaseModel):
    id: str
    name: str
    username: str
    role: int
    exp: datetime
    type: TokenTypeEnum


# --- responses ---
class AuthUserResponse(BaseResponseModel):
    id: str
    name: str
    username: str
    role: int
    email: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = False


class AuthLoginResponse(BaseResponseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    user: AuthUserResponse


class AuthRefreshTokenResponse(BaseResponseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
