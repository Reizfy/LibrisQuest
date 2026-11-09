from fastapi import Depends
from app.api.dependencies.repositories.user import get_user_repo
from app.api.dependencies.services.access_log import get_access_log_service
from app.services.auth import AuthService


def get_auth_service(
    user_repo=Depends(get_user_repo),
    acc_log_service=Depends(get_access_log_service),
):
    return AuthService(user_repo, acc_log_service)
