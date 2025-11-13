#!/usr/bin/env python3
"""
Test script for SmartMoney model
Verifies that anuraga is correctly set as admin
"""

import sys
sys.path.insert(0, 'app')

from models import SmartMoneyModel, User, UserRole, get_smart_money_instance


def test_smart_money_model():
    """Test SmartMoney model functionality"""
    print("Testing SmartMoney Model...")
    print("-" * 50)
    
    # Get SmartMoney instance
    smart_money = get_smart_money_instance()
    
    # Test 1: Check if anuraga is in admins list
    print("\n1. Testing if 'anuraga' is in admins list:")
    print(f"   Admins: {smart_money.admins}")
    assert "anuraga" in smart_money.admins, "anuraga should be in admins list"
    print("   ✓ PASS: anuraga is in admins list")
    
    # Test 2: Check if anuraga is admin
    print("\n2. Testing if 'anuraga' is identified as admin:")
    is_admin = smart_money.is_admin("anuraga")
    print(f"   Is anuraga admin? {is_admin}")
    assert is_admin, "anuraga should be identified as admin"
    print("   ✓ PASS: anuraga is identified as admin")
    
    # Test 3: Check if anuraga user exists and has admin role
    print("\n3. Testing if 'anuraga' user has admin role:")
    anuraga_user = smart_money.get_user("anuraga")
    print(f"   User found: {anuraga_user is not None}")
    if anuraga_user:
        print(f"   Username: {anuraga_user.username}")
        print(f"   Email: {anuraga_user.email}")
        print(f"   Role: {anuraga_user.role}")
        assert anuraga_user.role == UserRole.ADMIN, "anuraga user should have ADMIN role"
        print("   ✓ PASS: anuraga has admin role")
    else:
        print("   ✗ FAIL: anuraga user not found")
        sys.exit(1)
    
    # Test 4: Test adding another admin
    print("\n4. Testing adding another admin:")
    result = smart_money.add_admin("testuser")
    print(f"   Add result: {result}")
    print(f"   Updated admins: {smart_money.admins}")
    assert "testuser" in smart_money.admins, "testuser should be added to admins"
    print("   ✓ PASS: New admin added successfully")
    
    # Test 5: Test adding a regular user
    print("\n5. Testing adding a regular user:")
    test_user = User(
        username="regularuser",
        email="regular@test.com",
        role=UserRole.USER
    )
    result = smart_money.add_user(test_user)
    print(f"   Add result: {result}")
    print(f"   Total users: {len(smart_money.users)}")
    assert len(smart_money.users) >= 2, "Should have at least 2 users"
    print("   ✓ PASS: Regular user added successfully")
    
    # Test 6: Verify anuraga remains admin
    print("\n6. Final verification - anuraga is still admin:")
    print(f"   Admins: {smart_money.admins}")
    print(f"   Is anuraga admin? {smart_money.is_admin('anuraga')}")
    assert "anuraga" in smart_money.admins, "anuraga should still be in admins"
    print("   ✓ PASS: anuraga remains admin")
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
    print(f"\nSmartMoney Model Summary:")
    print(f"  Name: {smart_money.name}")
    print(f"  Description: {smart_money.description}")
    print(f"  Admins: {smart_money.admins}")
    print(f"  Total Users: {len(smart_money.users)}")
    print(f"  Created: {smart_money.created_at}")


if __name__ == "__main__":
    try:
        test_smart_money_model()
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
