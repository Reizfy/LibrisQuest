from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import config
from app.core.logger import get_logger

logger = get_logger(__name__)


class Database:
    apps_db_client: AsyncIOMotorClient = None

    # open connections
    @classmethod
    async def open_db_connection(cls) -> None:
        # open apps db connection
        logger.info(f"Connecting to Database ({config.APPS_DB_NAME})...")

        cls.apps_db_client = AsyncIOMotorClient(config.APPS_DB_URI)

        logger.info(f"Database {config.APPS_DB_NAME} is connected!")

    # close connections
    @classmethod
    async def close_db_connection(cls) -> None:
        # close apps db connection
        if cls.apps_db_client:
            logger.info(f"Closing Database connection ({config.APPS_DB_NAME})...")

            cls.apps_db_client.close()
            cls.apps_db_client = None

            logger.info(f"Database {config.APPS_DB_NAME} connection closed!")

    # get connections
    @classmethod
    def get_apps_db(cls) -> AsyncIOMotorDatabase:
        if not cls.apps_db_client:
            raise RuntimeError(
                f"Database client for {config.APPS_DB_NAME} not initialized"
            )

        return cls.apps_db_client[config.APPS_DB_NAME]


database = Database()
