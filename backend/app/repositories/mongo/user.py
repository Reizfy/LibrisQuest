import re
from typing import Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.logger import get_logger
from app.dto.user import UserFilter
from app.enums.common import SortOrderEnum
from app.models.user import User
from app.repositories.user import AbstractUserRepository
from app.utils.serializer import mongo_db_serializer

logger = get_logger(__name__)


class MongoUserRepository(AbstractUserRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    def _to_model(self, data: Optional[dict]) -> Optional[User]:
        if not data:
            return None

        new_data = data.copy()
        new_data["id"] = str(new_data.pop("_id"))

        serialized_user = mongo_db_serializer(new_data)

        return User(**serialized_user)

    def _to_mongo_dict(self, data: dict) -> dict:
        new_data = data.copy()

        if new_data.get("created_by"):
            new_data["created_by"] = ObjectId(new_data["created_by"])

        if new_data.get("updated_by"):
            new_data["updated_by"] = ObjectId(new_data["updated_by"])

        if new_data.get("updated_password_by"):
            new_data["updated_password_by"] = ObjectId(new_data["updated_password_by"])

        return new_data

    def _generate_query(self, filter: UserFilter) -> dict:
        query_list = []

        if filter.role:
            query_list.append({"role": filter.role.value})

        if filter.key:
            regex_keyword = re.escape(filter.key)
            query_list.append(
                {
                    "$or": [
                        {"name": {"$regex": regex_keyword, "$options": "i"}},
                        {"username": {"$regex": regex_keyword, "$options": "i"}},
                        {"email": {"$regex": regex_keyword, "$options": "i"}},
                    ]
                }
            )

        query = {"$and": query_list} if query_list else {}

        return query

    async def find_all(self, filter: UserFilter) -> tuple[list[User], int]:
        query = self._generate_query(filter)
        page = filter.page
        items = filter.items

        skip = (page - 1) * items
        sort_by = filter.sort_by.value
        sort_order = -1 if filter.sort_order == SortOrderEnum.DESC else 1

        # get data
        cursor = (
            self.collection.find(query)
            .skip(skip)
            .limit(items)
            .sort([(sort_by, sort_order)])
        )
        documents = await cursor.to_list(length=items)

        # counting total
        total = await self.collection.count_documents(query)

        # mapping
        users = [self._to_model(doc) for doc in documents]

        return users, total

    async def find_by_id(self, user_id: str) -> Optional[User]:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})

        return self._to_model(user)

    async def find_by_username(self, username: str) -> Optional[User]:
        user = await self.collection.find_one({"username": username})

        return self._to_model(user)

    async def create(self, user: User) -> str:
        try:
            payload = user.model_dump(exclude_unset=True)
            data = self._to_mongo_dict(payload)

            result = await self.collection.insert_one(data)

            return str(result.inserted_id)
        except Exception as err:
            logger.error(f"MongoDB insert query error: {str(err)}")
            raise

    async def update_by_id(self, user_id: str, payload: dict) -> bool:
        try:
            data = self._to_mongo_dict(payload)

            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)}, {"$set": data}
            )

            return result.matched_count > 0
        except Exception as err:
            logger.error(f"MongoDB update query error: {str(err)}")

            raise

    async def delete_by_id(self, user_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})

            return result.deleted_count > 0
        except Exception as err:
            logger.error(f"MongoDB delete query error: {str(err)}")

            raise
