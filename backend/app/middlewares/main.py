import asyncio
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from slowapi.errors import RateLimitExceeded
from app.core.exception import (
    CustomException,
    InvalidTokenException,
    UnauthorizedException,
)
from app.core.logger import get_logger
from app.dto.auth import AuthClaims
from app.dto.common import RequestContext
from app.enums.common import TokenTypeEnum
from app.integrations.telegram import TelegramIntegration
from app.middlewares.jwt.main import jwt_util
from app.services.notification import NotificationService

logger = get_logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)
telegram_integration = TelegramIntegration()
notif_service = NotificationService(telegram_integration)


class Middleware:
    @staticmethod
    def get_auth_user(token: str = Depends(oauth2_scheme)) -> AuthClaims:
        if not token:
            raise UnauthorizedException()

        try:
            auth_claims = jwt_util.parse_token(token)
            if auth_claims.type != TokenTypeEnum.ACCESS:
                raise InvalidTokenException()

            return auth_claims
        except Exception as err:
            logger.error(f"Failed to get auth user: {str(err)}")

            raise InvalidTokenException()

    @staticmethod
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled internal error")

        context = RequestContext(
            ip=request.client.host if request.client else None,
            port=request.client.port if request.client else None,
            url=str(request.url),
            method=request.method,
        )
        asyncio.create_task(
            notif_service.notify_internal_server_error(context, str(exc))
        )

        return JSONResponse(
            status_code=500,
            content={
                "err_code": "INTERNAL_SERVER",
            },
        )

    @staticmethod
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "err_code": exc.error_code,
            },
        )

    @staticmethod
    async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "err_code": "RATE_LIMIT_EXCEEDED",
            },
        )


middleware = Middleware()
