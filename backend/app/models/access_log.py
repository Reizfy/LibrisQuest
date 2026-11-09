from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AccessLog(BaseModel):
    id: Optional[str] = None
    user_id: str
    username: str
    ip_address: str
    user_agent: str
    created_at: Optional[datetime]
