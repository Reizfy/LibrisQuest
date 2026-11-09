from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None
    name: str
    username: str
    password: str
    is_active: bool
    role: int
    email: Optional[str] = None
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None
    created_at: datetime = None
    created_by: str = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    updated_password_at: Optional[datetime] = None
    updated_password_by: Optional[str] = None
