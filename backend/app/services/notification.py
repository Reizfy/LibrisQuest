from app.dto.common import RequestContext
from app.integrations.telegram import TelegramIntegration
from app.core.config import config
from app.utils.common import get_current_datetime


class NotificationService:
    def __init__(self, telegram_integration: TelegramIntegration):
        self.telegram_integration = telegram_integration

    async def notify_internal_server_error(
        self, context: RequestContext, message: str
    ) -> None:
        formatted_message = "<b>🔊DANGER</b>‼️‼️\n"
        formatted_message += "<b>SERVICE FASTAPI INTERNAL SERVER ERROR 🔥🔥</b>\n\n"
        formatted_message += "🗓️*{}*\n\n".format(
            get_current_datetime().replace(microsecond=0)
        )

        if context.ip:
            formatted_message += f"<b>IP ADDRESS:</b>\n{context.ip}\n\n"

        if context.port:
            formatted_message += f"<b>PORT:</b>\n{context.port}\n\n"

        if context.url:
            formatted_message += f"<b>URL:</b>\n{context.url}\n\n"

        if context.method:
            formatted_message += f"<b>METHOD:</b>\n{context.method}\n\n"

        formatted_message += f"<b>ERROR MESSAGE:</b>\n{message}\n\n"

        await self.telegram_integration.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=formatted_message,
            message_thread_id=config.TELEGRAM_MESSAGE_THREAD_ID,
        )
