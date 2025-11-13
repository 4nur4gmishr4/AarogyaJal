# SmartMoney Model Documentation

## Overview

The SmartMoney Model is a user management system integrated into the AarogyaJal backend. It provides functionality for managing users and their roles, with special focus on admin user management.

## Key Features

- **User Management**: Add, retrieve, and remove users
- **Admin Management**: Designate users as admins with special privileges
- **Role-Based Access**: Support for ADMIN, USER, and VIEWER roles
- **Built-in Admin**: `anuraga` is pre-configured as an admin user

## Models

### UserRole (Enum)
- `ADMIN`: Administrator with full access
- `USER`: Regular user with standard access
- `VIEWER`: Read-only access

### User
```python
class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    role: UserRole = UserRole.USER
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    is_active: bool = True
```

### SmartMoneyModel
```python
class SmartMoneyModel(BaseModel):
    id: Optional[int] = None
    name: str = "SmartMoney System"
    description: str = "Financial management and tracking system"
    admins: list[str] = Field(default_factory=lambda: ["anuraga"])
    users: list[User] = Field(default_factory=list)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
```

## API Endpoints

### GET /smartmoney
Get SmartMoney model information including admins and user count.

**Response:**
```json
{
  "name": "SmartMoney System",
  "description": "Financial management and tracking system for AarogyaJal",
  "admins": ["anuraga"],
  "total_users": 1,
  "created_at": "2025-11-01T11:23:27.874859",
  "updated_at": "2025-11-01T11:23:27.874898"
}
```

### GET /smartmoney/admins
Get list of all admins in the SmartMoney system.

**Response:**
```json
{
  "admins": ["anuraga"]
}
```

### GET /smartmoney/users
Get all users in the SmartMoney system.

**Response:**
```json
{
  "users": [
    {
      "username": "anuraga",
      "email": "anuraga@aarogyajal.com",
      "role": "admin",
      "is_active": true,
      "created_at": "2025-11-01T11:23:27.874880"
    }
  ]
}
```

### GET /smartmoney/users/{username}
Get specific user information.

**Response:**
```json
{
  "username": "anuraga",
  "email": "anuraga@aarogyajal.com",
  "role": "admin",
  "is_admin": true,
  "is_active": true,
  "created_at": "2025-11-01T11:23:27.874880"
}
```

### POST /smartmoney/users
Add a new user to the SmartMoney system.

**Request:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "role": "user",
  "is_active": true
}
```

**Response:**
```json
{
  "message": "User added successfully",
  "user": {
    "username": "newuser",
    "role": "user",
    "is_admin": false
  }
}
```

### POST /smartmoney/admins/{username}
Add a user as admin in the SmartMoney system.

**Response:**
```json
{
  "message": "'username' added as admin successfully",
  "admins": ["anuraga", "username"]
}
```

## Default Configuration

By default, the SmartMoney model is initialized with:
- **Name**: "SmartMoney System"
- **Description**: "Financial management and tracking system for AarogyaJal"
- **Admin User**: "anuraga" (username: anuraga, email: anuraga@aarogyajal.com, role: ADMIN)

## Usage Example

```python
from models import get_smart_money_instance, User, UserRole

# Get SmartMoney instance
smart_money = get_smart_money_instance()

# Check if anuraga is admin
print(smart_money.is_admin("anuraga"))  # True

# Get anuraga user details
anuraga = smart_money.get_user("anuraga")
print(f"Role: {anuraga.role}")  # Role: UserRole.ADMIN

# Add a new user
new_user = User(
    username="john",
    email="john@example.com",
    role=UserRole.USER
)
smart_money.add_user(new_user)

# Add another admin
smart_money.add_admin("jane")
print(smart_money.admins)  # ['anuraga', 'jane']
```

## Testing

Run the test suite to verify SmartMoney functionality:

```bash
cd backend
python test_smartmoney.py
python test_api_smartmoney.py
```

All tests should pass, confirming that:
1. `anuraga` is in the admins list
2. `anuraga` is identified as an admin
3. `anuraga` user has the ADMIN role
4. Admin management works correctly
5. User management works correctly

## Notes

- The SmartMoney model is initialized when the FastAPI app starts
- `anuraga` is automatically configured as an admin user
- Users in the admins list are automatically assigned the ADMIN role when added to the system
- All timestamps are in ISO 8601 format
