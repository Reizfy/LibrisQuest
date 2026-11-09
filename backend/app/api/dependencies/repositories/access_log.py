from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import database
from app.repositories.mongo.access_log import MongoAccessLogRepository


def get_access_log_repo(
    db: AsyncIOMotorDatabase = Depends(database.get_apps_db),
):
    return MongoAccessLogRepository(db)
