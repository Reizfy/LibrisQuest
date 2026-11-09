from datetime import datetime, timedelta, timezone
from jose import ExpiredSignatureError, jwt
from app.core.config import config
from app.core.exception import (
    ExpiredTokenException,
    InternalServerException,
    InvalidTokenException,
)
from app.core.logger import get_logger
from app.dto.auth import AuthClaims
from app.enums.common import TokenTypeEnum
from app.utils.common import get_current_datetime

logger = get_logger(__name__)


class JWTUtil:
    @staticmethod
    def create_token(
        id: str, name: str, username: str, role: int, duration: int, type: TokenTypeEnum
    ) -> str:
        try:
            auth_claims: AuthClaims = AuthClaims(
                id=id,
                name=name,
                username=username,
                role=role,
                exp=datetime.now(timezone.utc) + timedelta(minutes=duration),
                type=type,
            )

            token = jwt.encode(
                claims=auth_claims.model_dump(),
                key=config.AUTH_SECRET_KEY,
                algorithm=config.AUTH_ALGORITHM,
            )

            return token
        except Exception as err:
            logger.error(f"Failed to create token: {str(err)}")

            raise InternalServerException()

    @staticmethod
    def parse_token(token: str) -> AuthClaims:
        try:
            auth_claims: AuthClaims = jwt.decode(
                token=token,
                key=config.AUTH_SECRET_KEY,
                algorithms=config.AUTH_ALGORITHM,
            )

            return AuthClaims(**auth_claims)
        except ExpiredSignatureError as err:
            logger.error(f"Token expired: {str(err)}")

            raise ExpiredTokenException()
        except Exception as err:
            logger.error(f"Failed to parse token: {str(err)}")

            raise InvalidTokenException()


jwt_util = JWTUtil()
