from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class UserRole(str, Enum):
    """User roles in the system"""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class User(BaseModel):
    """User model for the system"""
    id: Optional[int] = None
    username: str
    email: str
    role: UserRole = UserRole.USER
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    is_active: bool = True


class SmartMoneyModel(BaseModel):
    """
    Smart Money Model - Financial tracking and management system
    This model manages users and their permissions in the financial system
    """
    id: Optional[int] = None
    name: str = "SmartMoney System"
    description: str = "Financial management and tracking system"
    admins: list[str] = Field(default_factory=lambda: ["anuraga"])
    users: list[User] = Field(default_factory=list)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    def add_admin(self, username: str) -> bool:
        """Add a user as admin to the SmartMoney system"""
        if username not in self.admins:
            self.admins.append(username)
            self.updated_at = datetime.now()
            return True
        return False
    
    def is_admin(self, username: str) -> bool:
        """Check if a user is an admin"""
        return username in self.admins
    
    def add_user(self, user: User) -> bool:
        """Add a user to the system"""
        # Check if user already exists
        existing_user = next((u for u in self.users if u.username == user.username), None)
        if existing_user:
            return False
        
        # Set role to admin if username is in admins list
        if user.username in self.admins:
            user.role = UserRole.ADMIN
        
        self.users.append(user)
        self.updated_at = datetime.now()
        return True
    
    def get_user(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return next((u for u in self.users if u.username == username), None)
    
    def remove_user(self, username: str) -> bool:
        """Remove a user from the system"""
        user = next((u for u in self.users if u.username == username), None)
        if user:
            self.users.remove(user)
            self.updated_at = datetime.now()
            return True
        return False


# Initialize the SmartMoney model with anuraga as admin
def get_smart_money_instance() -> SmartMoneyModel:
    """
    Factory function to get SmartMoney instance with anuraga as admin
    """
    smart_money = SmartMoneyModel(
        name="SmartMoney System",
        description="Financial management and tracking system for AarogyaJal",
        admins=["anuraga"]
    )
    
    # Add anuraga as admin user
    anuraga_user = User(
        id=1,
        username="anuraga",
        email="anuraga@aarogyajal.com",
        role=UserRole.ADMIN,
        is_active=True
    )
    smart_money.add_user(anuraga_user)
    
    return smart_money
