from app.dto.common import BaseRequestModel


# --- requests ---
class AccessLogCreate(BaseRequestModel):
    user_id: str
    username: str
    ip_address: str
    user_agent: str
