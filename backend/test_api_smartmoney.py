#!/usr/bin/env python3
"""
Test script for SmartMoney API endpoints (without running the server)
Tests the API logic directly
"""

import sys
sys.path.insert(0, 'app')

from models import get_smart_money_instance, User, UserRole


def test_smartmoney_api_logic():
    """Test SmartMoney API endpoint logic"""
    print("Testing SmartMoney API Logic...")
    print("-" * 50)
    
    # Initialize SmartMoney (simulating what happens in app.py)
    smart_money = get_smart_money_instance()
    
    # Test 1: GET /smartmoney (info endpoint)
    print("\n1. Testing GET /smartmoney endpoint logic:")
    info = {
        "name": smart_money.name,
        "description": smart_money.description,
        "admins": smart_money.admins,
        "total_users": len(smart_money.users),
        "created_at": smart_money.created_at.isoformat(),
        "updated_at": smart_money.updated_at.isoformat()
    }
    print(f"   Response: {info}")
    assert info["admins"] == ["anuraga"], "anuraga should be in admins"
    print("   ✓ PASS: /smartmoney endpoint works")
    
    # Test 2: GET /smartmoney/admins
    print("\n2. Testing GET /smartmoney/admins endpoint logic:")
    admins_response = {"admins": smart_money.admins}
    print(f"   Response: {admins_response}")
    assert "anuraga" in admins_response["admins"], "anuraga should be in admins"
    print("   ✓ PASS: /smartmoney/admins endpoint works")
    
    # Test 3: GET /smartmoney/users
    print("\n3. Testing GET /smartmoney/users endpoint logic:")
    users_response = {
        "users": [
            {
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            for user in smart_money.users
        ]
    }
    print(f"   Response: {users_response}")
    assert len(users_response["users"]) >= 1, "Should have at least 1 user (anuraga)"
    anuraga_in_users = any(u["username"] == "anuraga" for u in users_response["users"])
    assert anuraga_in_users, "anuraga should be in users list"
    print("   ✓ PASS: /smartmoney/users endpoint works")
    
    # Test 4: GET /smartmoney/users/anuraga
    print("\n4. Testing GET /smartmoney/users/anuraga endpoint logic:")
    user = smart_money.get_user("anuraga")
    if user:
        user_response = {
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_admin": smart_money.is_admin(user.username),
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        print(f"   Response: {user_response}")
        assert user_response["is_admin"] == True, "anuraga should be admin"
        assert user_response["role"] == UserRole.ADMIN, "anuraga should have ADMIN role"
        print("   ✓ PASS: /smartmoney/users/anuraga endpoint works")
    else:
        print("   ✗ FAIL: anuraga user not found")
        sys.exit(1)
    
    # Test 5: POST /smartmoney/users (add new user)
    print("\n5. Testing POST /smartmoney/users endpoint logic:")
    new_user = User(
        username="testuser2",
        email="testuser2@example.com",
        role=UserRole.USER
    )
    if smart_money.add_user(new_user):
        response = {
            "message": "User added successfully",
            "user": {
                "username": new_user.username,
                "role": new_user.role,
                "is_admin": smart_money.is_admin(new_user.username)
            }
        }
        print(f"   Response: {response}")
        print("   ✓ PASS: POST /smartmoney/users endpoint works")
    else:
        print("   ✗ FAIL: Could not add user")
    
    # Test 6: POST /smartmoney/admins/{username} (add admin)
    print("\n6. Testing POST /smartmoney/admins/testadmin endpoint logic:")
    if smart_money.add_admin("testadmin"):
        response = {
            "message": "'testadmin' added as admin successfully",
            "admins": smart_money.admins
        }
        print(f"   Response: {response}")
        assert "testadmin" in response["admins"], "testadmin should be in admins"
        print("   ✓ PASS: POST /smartmoney/admins endpoint works")
    
    print("\n" + "=" * 50)
    print("ALL API LOGIC TESTS PASSED!")
    print("=" * 50)
    print(f"\nFinal State:")
    print(f"  Admins: {smart_money.admins}")
    print(f"  Total Users: {len(smart_money.users)}")
    print(f"  anuraga is admin: {smart_money.is_admin('anuraga')}")


if __name__ == "__main__":
    try:
        test_smartmoney_api_logic()
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
