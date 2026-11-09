from fastapi import Depends
from app.api.dependencies.repositories.access_log import get_access_log_repo
from app.repositories.mongo.access_log import MongoAccessLogRepository
from app.services.access_log import AccessLogService


def get_access_log_service(
    acc_log_repo: MongoAccessLogRepository = Depends(get_access_log_repo),
):
    return AccessLogService(acc_log_repo)
