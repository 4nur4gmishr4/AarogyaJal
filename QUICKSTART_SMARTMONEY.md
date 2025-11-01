# QuickStart Guide: SmartMoney Model with Anuraga as Admin

## Overview
This guide shows you how to use the newly implemented SmartMoney model where **anuraga** is configured as the default administrator.

## Quick Verification

### 1. Verify the Implementation (Command Line)

```bash
cd backend
pip install -r requirements.txt
python verify_anuraga_admin.py
```

Expected output:
```
✓✓✓ SUCCESS: anuraga is correctly set as admin! ✓✓✓
```

### 2. Start the API Server

```bash
cd backend/app
# Create .env file with your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Start the server
python app.py
```

The server will start at `http://localhost:8000`

### 3. Test the SmartMoney Endpoints

#### Get System Information
```bash
curl http://localhost:8000/smartmoney
```

Response:
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

#### Check Who Are Admins
```bash
curl http://localhost:8000/smartmoney/admins
```

Response:
```json
{
  "admins": ["anuraga"]
}
```

#### Get Anuraga's User Details
```bash
curl http://localhost:8000/smartmoney/users/anuraga
```

Response:
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

#### List All Users
```bash
curl http://localhost:8000/smartmoney/users
```

Response:
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

#### Add a New User
```bash
curl -X POST http://localhost:8000/smartmoney/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "role": "user",
    "is_active": true
  }'
```

Response:
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

#### Add Another Admin
```bash
curl -X POST http://localhost:8000/smartmoney/admins/newadmin
```

Response:
```json
{
  "message": "'newadmin' added as admin successfully",
  "admins": ["anuraga", "newadmin"]
}
```

## Python Usage

### Basic Usage

```python
from models import get_smart_money_instance, User, UserRole

# Get the SmartMoney instance
smart_money = get_smart_money_instance()

# Check if anuraga is admin
print(smart_money.is_admin("anuraga"))  # True

# Get anuraga's details
anuraga = smart_money.get_user("anuraga")
print(f"Username: {anuraga.username}")
print(f"Role: {anuraga.role}")
print(f"Email: {anuraga.email}")

# Get list of admins
print(f"Admins: {smart_money.admins}")  # ['anuraga']
```

### Adding New Users

```python
# Create a new user
new_user = User(
    username="john",
    email="john@example.com",
    role=UserRole.USER
)

# Add the user
if smart_money.add_user(new_user):
    print("User added successfully!")
else:
    print("User already exists!")
```

### Managing Admins

```python
# Add a new admin
if smart_money.add_admin("jane"):
    print("Jane is now an admin!")
    print(f"Current admins: {smart_money.admins}")

# Check if someone is admin
if smart_money.is_admin("jane"):
    print("Jane has admin privileges")
```

## Running Tests

### Run All Tests

```bash
cd backend

# Model tests
python test_smartmoney.py

# API tests  
python test_api_smartmoney.py

# Final verification
python verify_anuraga_admin.py
```

All tests should pass and confirm that anuraga is properly configured as admin.

## Key Points

✅ **anuraga** is automatically configured as admin when the SmartMoney model initializes
✅ No manual configuration needed - it's built into the system
✅ anuraga has full admin privileges from the start
✅ The system supports multiple admins
✅ User roles are properly enforced (ADMIN, USER, VIEWER)

## Documentation

For more detailed information, see:
- `backend/SMARTMONEY_README.md` - Complete API documentation
- `backend/IMPLEMENTATION_SUMMARY.md` - Implementation details
- `backend/README.md` - Backend setup guide

## Troubleshooting

### Issue: Server won't start
**Solution**: Make sure you have set the `GEMINI_API_KEY` environment variable in the `.env` file.

### Issue: Tests fail
**Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: anuraga not showing as admin
**Solution**: This should not happen. If it does, the `get_smart_money_instance()` function guarantees anuraga is set as admin. Check that you're using the function correctly.

## Next Steps

1. Start the API server
2. Test the endpoints with curl or Postman
3. Integrate the SmartMoney API into your application
4. Add more users and admins as needed
5. Customize the model for your specific use case

---

**Status**: ✅ Fully implemented and tested
**Version**: 1.0.0
**Last Updated**: November 1, 2025
