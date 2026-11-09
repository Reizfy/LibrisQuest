from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Optional
import aiomysql
import pymysql.err
from app.core.config import config
from app.core.logger import get_logger

logger = get_logger(__name__)


class Database:
    pool: Optional[aiomysql.Pool] = None

    @classmethod
    async def open_db_connection(cls) -> None:
        """
        Initialize the asynchronous MySQL connection pool.
        Catches and logs connection errors gracefully.
        """
        logger.info(
            f"Connecting to MySQL database pool at {config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME} "
            f"(min_size={config.DB_POOL_MIN_SIZE}, max_size={config.DB_POOL_MAX_SIZE})..."
        )
        try:
            cls.pool = await aiomysql.create_pool(
                host=config.DB_HOST,
                port=config.DB_PORT,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                db=config.DB_NAME,
                minsize=config.DB_POOL_MIN_SIZE,
                maxsize=config.DB_POOL_MAX_SIZE,
                connect_timeout=config.DB_CONNECT_TIMEOUT,
                autocommit=True,
                charset="utf8mb4",
                cursorclass=aiomysql.DictCursor,
            )
            logger.info(
                f"MySQL database pool connected successfully to '{config.DB_NAME}'!"
            )
        except (
            aiomysql.Error,
            pymysql.err.OperationalError,
            OSError,
            ConnectionRefusedError,
        ) as err:
            cls.pool = None
            logger.error(
                f"Failed to connect to MySQL database at {config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}. "
                f"Error: {str(err)}"
            )

    @classmethod
    async def close_db_connection(cls) -> None:
        """
        Gracefully close all connections in the MySQL connection pool.
        """
        if cls.pool:
            logger.info(
                f"Closing MySQL connection pool for database '{config.DB_NAME}'..."
            )
            cls.pool.close()
            await cls.pool.wait_closed()
            cls.pool = None
            logger.info(
                f"MySQL connection pool for database '{config.DB_NAME}' closed successfully!"
            )

    @classmethod
    def get_pool(cls) -> aiomysql.Pool:
        """
        Retrieve the active connection pool. Raises RuntimeError if uninitialized.
        """
        if not cls.pool:
            raise RuntimeError(
                f"MySQL connection pool for database '{config.DB_NAME}' is not initialized. "
                "Ensure MySQL server is running and database configuration in .env is correct."
            )
        return cls.pool

    @classmethod
    @asynccontextmanager
    async def get_connection(cls) -> AsyncGenerator[aiomysql.Connection, None]:
        """
        Async context manager to acquire a connection from the pool.
        Automatically returns the connection to the pool upon exit.
        """
        pool = cls.get_pool()
        async with pool.acquire() as conn:
            yield conn

    @classmethod
    async def execute(cls, query: str, args: tuple = ()) -> int:
        """
        Helper method to execute an INSERT, UPDATE, or DELETE query and return affected row count.
        """
        async with cls.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                return cursor.rowcount

    @classmethod
    async def fetch_one(cls, query: str, args: tuple = ()) -> Optional[Dict[str, Any]]:
        """
        Helper method to execute a SELECT query and fetch a single dictionary row.
        """
        async with cls.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                return await cursor.fetchone()

    @classmethod
    async def fetch_all(cls, query: str, args: tuple = ()) -> List[Dict[str, Any]]:
        """
        Helper method to execute a SELECT query and fetch all dictionary rows.
        """
        async with cls.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                return await cursor.fetchall()

    # Legacy compatibility method
    @classmethod
    def get_apps_db(cls):
        if not cls.pool:
            logger.warning("Attempted to access database pool while uninitialized.")
        return cls.pool


database = Database()


async def get_db_connection() -> AsyncGenerator[aiomysql.Connection, None]:
    """
    FastAPI dependency yielding an acquired MySQL connection from the pool.
    """
    async with Database.get_connection() as conn:
        yield conn
