import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # apps db
    APPS_DB_URI: str = os.getenv("APPS_DB_URI")
    APPS_DB_NAME: str = os.getenv("APPS_DB_NAME")

    # auth
    AUTH_SECRET_KEY: str = os.getenv("AUTH_SECRET_KEY")
    AUTH_ALGORITHM: str = os.getenv("AUTH_ALGORITHM")
    AUTH_ACCESS_TOKEN_EXP: int = int(os.getenv("AUTH_ACCESS_TOKEN_EXP"))
    AUTH_REFRESH_TOKEN_EXP: int = int(os.getenv("AUTH_REFRESH_TOKEN_EXP"))
    AUTH_REFRESH_TOKEN_REMEMBER_EXP: int = int(
        os.getenv("AUTH_REFRESH_TOKEN_REMEMBER_EXP")
    )

    # telegram logs
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID")
    TELEGRAM_MESSAGE_THREAD_ID: str = os.getenv("TELEGRAM_MESSAGE_THREAD_ID")

    # whitelist domain
    ORIGINS: list[str] = [item.strip() for item in os.getenv("ORIGINS").split(",")]


config = Config()
