from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.logger import get_logger
from app.models.access_log import AccessLog
from app.repositories.access_log import AbstractAccessLogRepository

logger = get_logger(__name__)


class MongoAccessLogRepository(AbstractAccessLogRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["access_logs"]

    def _to_mongo_dict(self, data: dict) -> dict:
        new_data = data.copy()

        if new_data.get("user_id"):
            new_data["user_id"] = ObjectId(new_data["user_id"])

        return new_data

    async def create(self, data: AccessLog) -> str:
        try:
            payload = data.model_dump(exclude_unset=True)
            data = self._to_mongo_dict(payload)

            result = await self.collection.insert_one(data)

            return str(result.inserted_id)
        except Exception as err:
            logger.error(f"Database insert query error: {str(err)}")

            raise
