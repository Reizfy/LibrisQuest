from datetime import datetime
from bson import ObjectId


def mongo_db_serializer(data: dict) -> dict:
    result = {}

    for key, value in data.items():
        if isinstance(value, ObjectId):
            result[key if key != "_id" else "id"] = str(value)

        elif isinstance(value, datetime):
            result[key] = value.isoformat()

        else:
            result[key] = value

    return result
