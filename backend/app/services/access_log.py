from app.core.exception import InternalServerException
from app.dto.access_log import AccessLogCreate
from app.models.access_log import AccessLog
from app.repositories.access_log import AbstractAccessLogRepository
from app.utils.common import get_current_datetime


class AccessLogService:
    def __init__(self, acc_log_repo: AbstractAccessLogRepository):
        self.acc_log_repo = acc_log_repo

    async def create_access_log(self, data: AccessLogCreate) -> str:
        new_access_log = AccessLog(
            user_id=data.user_id,
            username=data.username,
            ip_address=data.ip_address,
            user_agent=data.user_agent,
            created_at=get_current_datetime(),
        )

        # creating access log
        inserted_id = await self.acc_log_repo.create(new_access_log)
        if not inserted_id:
            raise InternalServerException()

        return inserted_id
