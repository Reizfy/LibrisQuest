from fastapi import Depends
from app.api.dependencies.repositories.user import get_user_repo
from app.repositories.mongo.user import MongoUserRepository
from app.services.user import UserService


def get_user_service(user_repo: MongoUserRepository = Depends(get_user_repo)):
    return UserService(user_repo)
