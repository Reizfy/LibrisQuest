# --- base ---
class CustomException(Exception):
    def __init__(self, error_code: str, status_code: int = 500):
        self.error_code = error_code
        self.status_code = status_code


# --- common ---
class InternalServerException(CustomException):
    def __init__(self):
        super().__init__(error_code="INTERNAL_SERVER", status_code=500)


class UserInactiveException(CustomException):
    def __init__(self):
        super().__init__(error_code="USER_INACTIVE", status_code=400)


class UnauthorizedException(CustomException):
    def __init__(self):
        super().__init__(error_code="UNAUTHORIZED", status_code=401)


class ForbiddenException(CustomException):
    def __init__(self):
        super().__init__(error_code="FORBIDDEN_ACCESS", status_code=403)


class ForbiddenFileException(CustomException):
    def __init__(self):
        super().__init__(error_code="FORBIDDEN_FILE", status_code=400)


class ExternalApiException(CustomException):
    def __init__(self):
        super().__init__(error_code="EXTERNAL_API", status_code=500)


class PayloadRequiredException(CustomException):
    def __init__(self):
        super().__init__(error_code="REQUIRED_PAYLOAD", status_code=400)


# --- invalid ---
class InvalidAuthException(CustomException):
    def __init__(self):
        super().__init__(error_code="INVALID_AUTH", status_code=400)


class InvalidTokenException(CustomException):
    def __init__(self):
        super().__init__(error_code="INVALID_TOKEN", status_code=400)


class InvalidOldPasswordException(CustomException):
    def __init__(self):
        super().__init__(error_code="INVALID_OLD_PASSWORD", status_code=400)


# --- not found ---
class DataNotFoundException(CustomException):
    def __init__(self):
        super().__init__(error_code="DATA_NOT_FOUND", status_code=400)


# --- exist ---
class DataExistException(CustomException):
    def __init__(self):
        super().__init__(error_code="DATA_EXIST", status_code=400)


class UsernameExistException(CustomException):
    def __init__(self):
        super().__init__(error_code="USERNAME_EXIST", status_code=400)


# --- expired ---
class ExpiredTokenException(CustomException):
    def __init__(self):
        super().__init__(error_code="TOKEN_EXPIRED", status_code=400)
