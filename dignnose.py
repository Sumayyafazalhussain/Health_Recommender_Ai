# diagnose_auth_issue.py
"""
Diagnostic Script - Find exactly why auth router isn't loading
"""

import sys
import os

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_step(step_num, description, test_func):
    """Run a test step and report results"""
    print(f"\n{step_num}. {description}")
    try:
        result = test_func()
        if result:
            print("   ✅ PASS")
            return True
        else:
            print("   ❌ FAIL")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

print_header("JWT AUTHENTICATION DIAGNOSTIC TOOL")
print("This will help identify exactly why your auth router isn't loading")

# Test 1: Check if auth.py file exists
def check_auth_file():
    path = "app/routes/auth.py"
    exists = os.path.exists(path)
    if exists:
        size = os.path.getsize(path)
        print(f"   File exists: {path} ({size} bytes)")
        return True
    else:
        print(f"   File NOT FOUND: {path}")
        return False

# Test 2: Check if __init__.py exists
def check_init_file():
    path = "app/routes/__init__.py"
    exists = os.path.exists(path)
    if exists:
        print(f"   File exists: {path}")
        return True
    else:
        print(f"   File NOT FOUND: {path}")
        print("   Creating it now...")
        try:
            with open(path, 'w') as f:
                f.write("# Routes package\n")
            print("   ✅ Created __init__.py")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create: {e}")
            return False

# Test 3: Check Python syntax in auth.py
def check_syntax():
    try:
        with open("app/routes/auth.py", 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, "app/routes/auth.py", "exec")
        print("   No syntax errors found")
        return True
    except SyntaxError as e:
        print(f"   Syntax error at line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"   Error reading file: {e}")
        return False

# Test 4: Try importing auth module
def test_import_auth():
    try:
        from app.routes import auth
        print(f"   Successfully imported: {auth}")
        return True
    except ImportError as e:
        print(f"   Import failed: {e}")
        return False
    except Exception as e:
        print(f"   Unexpected error: {e}")
        return False

# Test 5: Check if router exists in auth module
def check_router_exists():
    try:
        from app.routes import auth
        if hasattr(auth, 'router'):
            print(f"   Router found: {auth.router}")
            print(f"   Router prefix: {auth.router.prefix}")
            return True
        else:
            print("   Router NOT FOUND in auth module")
            return False
    except Exception as e:
        print(f"   Error: {e}")
        return False

# Test 6: Check dependencies
def check_dependencies():
    missing = []
    try:
        import jose
        print("   ✅ python-jose installed")
    except ImportError:
        missing.append("python-jose")
    
    try:
        import passlib
        print("   ✅ passlib installed")
    except ImportError:
        missing.append("passlib")
    
    try:
        from fastapi.security import HTTPBearer
        print("   ✅ fastapi.security available")
    except ImportError:
        missing.append("fastapi.security")
    
    if missing:
        print(f"   ❌ Missing packages: {', '.join(missing)}")
        return False
    return True

# Test 7: Check if database models exist
def check_database_models():
    try:
        from app.db.neon_connection import User
        print(f"   User model exists: {User}")
        return True
    except ImportError as e:
        print(f"   User model not found: {e}")
        return False

# Test 8: Check if user models exist
def check_user_models():
    try:
        from app.models.user_model import UserCreate, UserLogin, Token
        print("   ✅ All user models found")
        return True
    except ImportError as e:
        print(f"   User models not found: {e}")
        return False

# Test 9: Check if auth service exists
def check_auth_service():
    try:
        from app.services.auth_service import get_password_hash, verify_password
        print("   ✅ Auth service functions found")
        return True
    except ImportError as e:
        print(f"   Auth service not found: {e}")
        return False

# Test 10: Check config
def check_config():
    try:
        from app.config import settings
        has_secret = bool(settings.SECRET_KEY)
        has_db = bool(settings.DATABASE_URL)
        print(f"   SECRET_KEY: {'Set' if has_secret else 'NOT SET'}")
        print(f"   DATABASE_URL: {'Set' if has_db else 'NOT SET'}")
        return has_secret and has_db
    except Exception as e:
        print(f"   Config error: {e}")
        return False

# Run all tests
print("\n" + "="*70)
print("RUNNING DIAGNOSTICS...")
print("="*70)

results = []
results.append(test_step("TEST 1", "Check auth.py file exists", check_auth_file))
results.append(test_step("TEST 2", "Check __init__.py exists", check_init_file))
results.append(test_step("TEST 3", "Check Python syntax", check_syntax))
results.append(test_step("TEST 4", "Import auth module", test_import_auth))
results.append(test_step("TEST 5", "Check router exists", check_router_exists))
results.append(test_step("TEST 6", "Check dependencies", check_dependencies))
results.append(test_step("TEST 7", "Check database models", check_database_models))
results.append(test_step("TEST 8", "Check user models", check_user_models))
results.append(test_step("TEST 9", "Check auth service", check_auth_service))
results.append(test_step("TEST 10", "Check configuration", check_config))

# Summary
print_header("DIAGNOSTIC SUMMARY")
passed = sum(results)
total = len(results)

print(f"\nTests Passed: {passed}/{total}")
print("\nDetailed Results:")
test_names = [
    "Auth file exists",
    "__init__.py exists",
    "Python syntax valid",
    "Auth module imports",
    "Router exists",
    "Dependencies installed",
    "Database models",
    "User models",
    "Auth service",
    "Configuration"
]

for i, (name, result) in enumerate(zip(test_names, results), 1):
    icon = "✅" if result else "❌"
    print(f"   {icon} {i}. {name}")

print("\n" + "="*70)

# Recommendations
if passed < total:
    print("\n🔧 RECOMMENDED ACTIONS:")
    
    if not results[0]:  # auth.py doesn't exist
        print("\n1. CREATE app/routes/auth.py")
        print("   - Copy the auth.py file I provided")
        print("   - Place it at: app/routes/auth.py")
    
    if not results[1]:  # __init__.py doesn't exist
        print("\n2. CREATE app/routes/__init__.py")
        print("   - This file has been created for you")
        print("   - If you see errors, create it manually (can be empty)")
    
    if not results[2]:  # Syntax error
        print("\n3. FIX SYNTAX ERRORS in auth.py")
        print("   - Check the error message above")
        print("   - Make sure you copied the ENTIRE file")
        print("   - Check for missing quotes, brackets, or colons")
    
    if not results[3]:  # Import failed
        print("\n4. FIX IMPORT ERRORS")
        print("   - Check all previous tests passed")
        print("   - Make sure you're in the project root directory")
    
    if not results[5]:  # Dependencies missing
        print("\n5. INSTALL MISSING DEPENDENCIES")
        print("   pip install python-jose[cryptography]==3.3.0")
        print("   pip install passlib[bcrypt]==1.7.4")
        print("   pip install python-multipart==0.0.6")
    
    if not results[6]:  # Database models
        print("\n6. CHECK DATABASE CONNECTION")
        print("   - Verify app/db/neon_connection.py exists")
        print("   - Check DATABASE_URL in .env")
    
    if not results[7]:  # User models
        print("\n7. CHECK USER MODELS")
        print("   - Verify app/models/user_model.py exists")
        print("   - Make sure it has UserCreate, UserLogin, Token")
    
    if not results[8]:  # Auth service
        print("\n8. CHECK AUTH SERVICE")
        print("   - Verify app/services/auth_service.py exists")
        print("   - Make sure it has get_password_hash, verify_password")
    
    if not results[9]:  # Config
        print("\n9. CHECK CONFIGURATION")
        print("   - Verify .env file exists")
        print("   - Make sure SECRET_KEY and DATABASE_URL are set")

else:
    print("\n✅ ALL TESTS PASSED!")
    print("\n🎉 Your authentication setup is correct!")
    print("\nIf you're still getting 404 errors:")
    print("   1. Make sure you updated app/main.py")
    print("   2. Restart your server completely")
    print("   3. Check server logs for import errors")

print("="*70)
print("\n💡 NEXT STEPS:")
print("   1. Fix any issues shown above")
print("   2. Restart your server: python run.py")
print("   3. Test again: python test_jwt_auth.py")
print("="*70 + "\n")