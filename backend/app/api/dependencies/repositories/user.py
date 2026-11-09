from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import database
from app.repositories.mongo.user import MongoUserRepository


def get_user_repo(
    db: AsyncIOMotorDatabase = Depends(database.get_apps_db),
):
    return MongoUserRepository(db)
