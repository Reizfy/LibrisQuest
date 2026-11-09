from abc import ABC, abstractmethod
from app.models.access_log import AccessLog


class AbstractAccessLogRepository(ABC):
    @abstractmethod
    async def create(self, data: AccessLog) -> str:
        """Create new access log"""
        pass
