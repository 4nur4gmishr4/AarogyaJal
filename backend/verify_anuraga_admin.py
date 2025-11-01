#!/usr/bin/env python3
"""
Final verification that anuraga is admin in SmartMoney model
"""

import sys
sys.path.insert(0, 'app')

from models import get_smart_money_instance

def main():
    print("=" * 60)
    print("FINAL VERIFICATION: Anuraga as Admin in SmartMoney Model")
    print("=" * 60)
    
    # Get the SmartMoney instance
    smart_money = get_smart_money_instance()
    
    # Verification checks
    print("\n✓ SmartMoney Model Information:")
    print(f"  Name: {smart_money.name}")
    print(f"  Description: {smart_money.description}")
    
    print("\n✓ Admin Verification:")
    print(f"  Admins list: {smart_money.admins}")
    print(f"  'anuraga' in admins list: {('anuraga' in smart_money.admins)}")
    print(f"  smart_money.is_admin('anuraga'): {smart_money.is_admin('anuraga')}")
    
    print("\n✓ User Verification:")
    anuraga_user = smart_money.get_user('anuraga')
    if anuraga_user:
        print(f"  Username: {anuraga_user.username}")
        print(f"  Email: {anuraga_user.email}")
        print(f"  Role: {anuraga_user.role}")
        print(f"  Is Active: {anuraga_user.is_active}")
        print(f"  Created At: {anuraga_user.created_at}")
    else:
        print("  ERROR: anuraga user not found!")
        sys.exit(1)
    
    # Final assertion
    print("\n" + "=" * 60)
    assert 'anuraga' in smart_money.admins, "FAIL: anuraga not in admins"
    assert smart_money.is_admin('anuraga'), "FAIL: anuraga not identified as admin"
    assert anuraga_user is not None, "FAIL: anuraga user not found"
    assert str(anuraga_user.role) == "UserRole.ADMIN", "FAIL: anuraga doesn't have ADMIN role"
    
    print("✓✓✓ SUCCESS: anuraga is correctly set as admin! ✓✓✓")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n✗✗✗ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
