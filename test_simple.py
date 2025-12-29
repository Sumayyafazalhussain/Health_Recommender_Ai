# test_complete.py
import os

print("🔧 COMPLETE SYSTEM TEST")
print("="*50)

# 1. Check .env file
print("\n1. Checking .env file...")
if os.path.exists(".env"):
    with open(".env", "r") as f:
        content = f.read()
        if "DATABASE_URL" in content:
            print("✅ .env file exists and has DATABASE_URL")
        else:
            print("⚠️ .env file exists but missing DATABASE_URL")
else:
    print("❌ .env file not found")

# 2. Check config
print("\n2. Checking config.py...")
try:
    from app.config import settings
    print(f"✅ Config loaded: DATABASE_URL={'Set' if settings.DATABASE_URL else 'Not set'}")
    if settings.DATABASE_URL:
        print(f"   URL: {settings.DATABASE_URL[:50]}...")
except Exception as e:
    print(f"❌ Config error: {e}")

# 3. Test database connection
print("\n3. Testing database connection...")
try:
    from app.db.neon_connection import test_connection
    print("✅ test_connection imported")
    
    # Try to connect
    if test_connection():
        print("✅ Database connection: SUCCESS")
    else:
        print("❌ Database connection: FAILED")
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Connection error: {e}")

# 4. Test Neon service
print("\n4. Testing Neon service...")
try:
    from app.services.neon_service import neon_db_service
    print("✅ Neon service imported")
    
    # Test health check
    health = neon_db_service.health_check()
    print(f"✅ Health check: {health['status']}")
    print(f"   Counts: {health.get('counts', {})}")
except Exception as e:
    print(f"❌ Neon service error: {e}")

print("\n" + "="*50)
print("🎉 Test complete!")
print("\n💡 If all tests pass, your app should work!")
print("="*50)