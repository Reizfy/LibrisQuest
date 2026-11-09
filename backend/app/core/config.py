import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Application
    APP_NAME: str = os.getenv("APP_NAME", "LibrisQuest")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # MySQL Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "librisquest_db")
    DB_POOL_MIN_SIZE: int = int(os.getenv("DB_POOL_MIN_SIZE", "1"))
    DB_POOL_MAX_SIZE: int = int(os.getenv("DB_POOL_MAX_SIZE", "10"))
    DB_CONNECT_TIMEOUT: int = int(os.getenv("DB_CONNECT_TIMEOUT", "10"))

    # Legacy / Compatibility Configuration
    APPS_DB_NAME: str = os.getenv("APPS_DB_NAME", DB_NAME)
    APPS_DB_URI: str = os.getenv(
        "APPS_DB_URI",
        f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )

    # Auth & Security (JWT)
    AUTH_SECRET_KEY: str = os.getenv(
        "AUTH_SECRET_KEY", "librisquest-insecure-dev-secret-key-change-me"
    )
    AUTH_ALGORITHM: str = os.getenv("AUTH_ALGORITHM", "HS256")
    AUTH_ACCESS_TOKEN_EXP: int = int(os.getenv("AUTH_ACCESS_TOKEN_EXP", "1440"))
    AUTH_REFRESH_TOKEN_EXP: int = int(os.getenv("AUTH_REFRESH_TOKEN_EXP", "10080"))
    AUTH_REFRESH_TOKEN_REMEMBER_EXP: int = int(
        os.getenv("AUTH_REFRESH_TOKEN_REMEMBER_EXP", "43200")
    )

    # Telegram logs & alerts (Optional)
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    TELEGRAM_MESSAGE_THREAD_ID: str = os.getenv("TELEGRAM_MESSAGE_THREAD_ID", "")

    # Whitelist CORS Origins
    ORIGINS: list[str] = [
        item.strip()
        for item in os.getenv(
            "ORIGINS",
            "http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:8000",
        ).split(",")
        if item.strip()
    ]


config = Config()
