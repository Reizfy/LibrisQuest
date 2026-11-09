from abc import ABC, abstractmethod
from typing import Optional
from app.dto.user import UserFilter
from app.models.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def find_all(self, filter: UserFilter) -> tuple[list[User], int]:
        """Get all user with pagination"""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass

    @abstractmethod
    async def create(self, user: User) -> Optional[str]:
        """Create new user"""
        pass

    @abstractmethod
    async def update_by_id(self, user_id: str, payload: dict) -> Optional[bool]:
        """Update user"""
        pass

    @abstractmethod
    async def delete_by_id(self, user_id: str) -> bool:
        """Delete user"""
        pass
