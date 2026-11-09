from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


class BaseRequestModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def strip_strings(cls, value):
        if isinstance(value, str):
            return value.strip()

        return value


class BaseResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Pagination(BaseResponseModel):
    page: int
    items: int
    total: int


class RequestContext(BaseModel):
    ip: Optional[str] = None
    port: Optional[int] = None
    user_agent: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = None
