import asyncio
from app.core.config import config
from app.core.exception import (
    InvalidAuthException,
    InvalidTokenException,
    UserInactiveException,
)
from app.dto.common import RequestContext
from app.dto.access_log import AccessLogCreate
from app.enums.common import TokenTypeEnum
from app.middlewares.jwt.main import jwt_util
from app.middlewares.main import AuthClaims
from app.models.user import User
from app.repositories.user import AbstractUserRepository
from app.services.access_log import AccessLogService
from app.utils.password import verify_hash_password


class AuthService:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        acc_log_service: AccessLogService,
    ):
        self.user_repo = user_repo
        self.acc_log_service = acc_log_service

    async def login(
        self,
        context: RequestContext,
        username: str,
        password: str,
        is_remember: bool = False,
    ) -> tuple[str, str, User]:
        # check existing user
        user: User = await self.user_repo.find_by_username(username=username)
        if not user:
            raise InvalidAuthException()

        # check user status
        if not user.is_active:
            raise UserInactiveException()

        # verify password
        if not verify_hash_password(
            plain_password=password, hashed_password=user.password
        ):
            raise InvalidAuthException()

        # create access & refresh token
        access_token = jwt_util.create_token(
            id=user.id,
            name=user.name,
            username=user.username,
            role=user.role,
            duration=config.AUTH_ACCESS_TOKEN_EXP,
            type=TokenTypeEnum.ACCESS.value,
        )

        refresh_token_exp = (
            config.AUTH_REFRESH_TOKEN_REMEMBER_EXP
            if is_remember
            else config.AUTH_REFRESH_TOKEN_EXP
        )
        refresh_token = jwt_util.create_token(
            id=user.id,
            name=user.name,
            username=user.username,
            role=user.role,
            duration=refresh_token_exp,
            type=TokenTypeEnum.REFRESH.value,
        )

        # creating access log
        access_log = AccessLogCreate(
            user_id=user.id,
            username=user.username,
            ip_address=context.ip,
            user_agent=context.user_agent,
        )
        asyncio.create_task(self.acc_log_service.create_access_log(data=access_log))

        return access_token, refresh_token, user

    async def refresh_token(self, refresh_token: str) -> tuple[str, str]:
        # parse token
        auth_claims: AuthClaims = jwt_util.parse_token(refresh_token)

        # check token type
        if auth_claims.type != TokenTypeEnum.REFRESH.value:
            raise InvalidTokenException()

        # check existing user
        user = await self.user_repo.find_by_id(auth_claims.id)
        if not user:
            raise InvalidAuthException()

        # check user status
        if not user.is_active:
            raise UserInactiveException()

        # create access & refresh token
        access_token = jwt_util.create_token(
            id=user.id,
            name=user.name,
            username=user.username,
            role=user.role,
            duration=config.AUTH_ACCESS_TOKEN_EXP,
            type=TokenTypeEnum.ACCESS.value,
        )
        refresh_token = jwt_util.create_token(
            id=user.id,
            name=user.name,
            username=user.username,
            role=user.role,
            duration=config.AUTH_REFRESH_TOKEN_EXP,
            type=TokenTypeEnum.REFRESH.value,
        )

        return access_token, refresh_token
