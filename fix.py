# fix_failing_tests.py
"""
Fix All Failing Tests
This script will fix tests 4, 8, 9, and 10 from your diagnostic
"""

import os
import shutil

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def backup_file(filepath):
    """Create backup of existing file"""
    if os.path.exists(filepath):
        backup_path = filepath + ".backup"
        try:
            shutil.copy2(filepath, backup_path)
            print(f"   ✅ Backed up: {filepath} → {backup_path}")
            return True
        except Exception as e:
            print(f"   ❌ Backup failed: {e}")
            return False
    return True

def check_file_exists(filepath):
    """Check if a file exists"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"   ✅ Found: {filepath} ({size} bytes)")
        return True
    else:
        print(f"   ❌ Missing: {filepath}")
        return False

print_header("FIXING FAILING TESTS")

# ============================================================
# FIX TEST 8: User Models
# ============================================================
print_header("FIX TEST 8: User Models")

user_model_path = "app/models/user_model.py"

if check_file_exists(user_model_path):
    print("\n   📋 Checking if user_model.py has required classes...")
    
    try:
        with open(user_model_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_classes = ['UserCreate', 'UserLogin', 'Token', 'TokenData']
        missing = []
        
        for cls in required_classes:
            if f"class {cls}" not in content:
                missing.append(cls)
        
        if missing:
            print(f"   ❌ Missing classes: {', '.join(missing)}")
            print("\n   🔧 ACTION REQUIRED:")
            print("   Replace app/models/user_model.py with the new user_model.py file provided")
        else:
            print(f"   ✅ All required classes found")
    
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
else:
    print("\n   🔧 ACTION REQUIRED:")
    print("   Copy the user_model.py file to app/models/user_model.py")

# ============================================================
# FIX TEST 9: Auth Service
# ============================================================
print_header("FIX TEST 9: Auth Service")

auth_service_path = "app/services/auth_service.py"

if check_file_exists(auth_service_path):
    print("\n   📋 Checking if auth_service.py has required functions...")
    
    try:
        with open(auth_service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_functions = [
            'get_password_hash',
            'verify_password',
            'create_access_token',
            'verify_token'
        ]
        missing = []
        
        for func in required_functions:
            if f"def {func}" not in content:
                missing.append(func)
        
        if missing:
            print(f"   ❌ Missing functions: {', '.join(missing)}")
            print("\n   🔧 ACTION REQUIRED:")
            print("   Replace app/services/auth_service.py with the new auth_service.py file provided")
        else:
            print(f"   ✅ All required functions found")
    
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
else:
    print("\n   🔧 ACTION REQUIRED:")
    print("   Copy the auth_service.py file to app/services/auth_service.py")

# ============================================================
# FIX TEST 10: Configuration
# ============================================================
print_header("FIX TEST 10: Configuration")

config_path = "app/config.py"

if check_file_exists(config_path):
    print("\n   📋 Checking configuration...")
    
    try:
        # Import and check settings
        from app.config import settings
        
        has_secret = bool(settings.SECRET_KEY and settings.SECRET_KEY != "your-fallback-secret-key-change-this-in-production")
        has_db = bool(settings.DATABASE_URL)
        
        if has_secret:
            print(f"   ✅ SECRET_KEY: Set")
        else:
            print(f"   ❌ SECRET_KEY: Not set or using default")
        
        if has_db:
            print(f"   ✅ DATABASE_URL: Set")
        else:
            print(f"   ❌ DATABASE_URL: Not set")
        
        if not has_secret or not has_db:
            print("\n   🔧 ACTION REQUIRED:")
            print("   1. Make sure .env file exists in project root")
            print("   2. Add these lines to .env:")
            print("      SECRET_KEY=your_secret_key_here")
            print("      DATABASE_URL=your_database_url_here")
            print("   3. Or replace app/config.py with the new config.py file provided")
    
    except Exception as e:
        print(f"   ❌ Error importing config: {e}")
        print("\n   🔧 ACTION REQUIRED:")
        print("   Replace app/config.py with the new config.py file provided")
else:
    print("\n   🔧 ACTION REQUIRED:")
    print("   Copy the config.py file to app/config.py")

# ============================================================
# FIX TEST 4: Import Errors
# ============================================================
print_header("FIX TEST 4: Import Errors")

print("\n   📋 Testing imports after fixes...")

# Test 1: Import config
try:
    from app.config import settings
    print("   ✅ Can import app.config.settings")
except Exception as e:
    print(f"   ❌ Cannot import config: {e}")

# Test 2: Import user models
try:
    from app.models.user_model import UserCreate, UserLogin, Token
    print("   ✅ Can import user models")
except Exception as e:
    print(f"   ❌ Cannot import user models: {e}")

# Test 3: Import auth service
try:
    from app.services.auth_service import get_password_hash, verify_password
    print("   ✅ Can import auth service")
except Exception as e:
    print(f"   ❌ Cannot import auth service: {e}")

# Test 4: Import auth router
try:
    from app.routes import auth
    print("   ✅ Can import auth router")
    if hasattr(auth, 'router'):
        print(f"   ✅ Router exists with prefix: {auth.router.prefix}")
    else:
        print("   ❌ Router not found in auth module")
except Exception as e:
    print(f"   ❌ Cannot import auth router: {e}")

# ============================================================
# SUMMARY
# ============================================================
print_header("SUMMARY & NEXT STEPS")

print("""
📋 FILES TO REPLACE:

1. app/models/user_model.py
   - Replace with: user_model.py (provided)
   
2. app/services/auth_service.py
   - Replace with: auth_service.py (provided)
   
3. app/config.py
   - Replace with: config.py (provided)
   OR ensure .env has SECRET_KEY and DATABASE_URL

🔧 HOW TO REPLACE FILES:

Windows:
   1. Open file in Notepad++
   2. Delete ALL content (Ctrl+A, Delete)
   3. Copy NEW content from provided file
   4. Save (Ctrl+S)

🧪 AFTER REPLACING:

1. Run diagnostic again:
   python diagnose_auth_issue.py
   
2. All 10 tests should pass
   
3. Restart server:
   python run.py
   
4. Test authentication:
   python test_jwt_auth.py

✅ EXPECTED RESULT:

   Tests Passed: 10/10
   All authentication endpoints working!
""")

print("="*70 + "\n")