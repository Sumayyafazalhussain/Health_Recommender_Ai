# check_imports.py
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Checking Python imports...")
print("="*50)

modules_to_check = [
    "app.routes.auth",
    "app.config",
    "app.db.neon_connection",
    "app.services.auth_service",
    "app.services.user_service",
    "app.models.user_model"
]

for module_name in modules_to_check:
    try:
        __import__(module_name)
        print(f"✅ {module_name}")
    except ImportError as e:
        print(f"❌ {module_name}: {e}")
    except SyntaxError as e:
        print(f"❌ {module_name} has syntax error: {e}")
    except Exception as e:
        print(f"❌ {module_name}: {type(e).__name__}: {e}")

print("\n📁 Checking directory structure...")
expected_dirs = [
    "app",
    "app/routes",
    "app/services",
    "app/models",
    "app/db"
]

for dir_name in expected_dirs:
    if os.path.exists(dir_name):
        print(f"✅ {dir_name}/")
    else:
        print(f"❌ {dir_name}/ (missing)")

print("\n" + "="*50)
print("💡 If imports fail, check:")
print("   1. You're in the right directory")
print("   2. All required packages are installed")
print("   3. File permissions are correct")
print("="*50)