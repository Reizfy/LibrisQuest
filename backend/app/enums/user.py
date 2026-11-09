from enum import Enum


class UserRoleEnum(int, Enum):
    ADMIN = 1
    VIEWER = 2


class UserSortByEnum(str, Enum):
    CREATED_AT = "created_at"
    NAME = "name"
    USERNAME = "username"
