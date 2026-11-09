from enum import Enum


class SortOrderEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"


class TokenTypeEnum(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
