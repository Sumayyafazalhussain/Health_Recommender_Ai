
# # run.py
# import uvicorn

# if __name__ == "__main__":
#     print("\n" + "="*60)
#     print("🏥 HEALTH RECOMMENDER AI - Neon PostgreSQL")
#     print("="*60)
    
#     uvicorn.run(
#         "app.main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True,
#         log_level="info"
#     )













# import uvicorn
# import os
# import sys

# # Add the current directory to Python path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# if __name__ == "__main__":
#     print("\n" + "="*60)
#     print("🏥 HEALTH RECOMMENDER AI - JWT Authentication")
#     print("="*60)
    
#     # Test imports before starting
#     try:
#         from app.main import app
#         print("✅ App imported successfully")
        
#         # Test database connection
#         from app.db.neon_connection import test_connection
#         if test_connection():
#             print("✅ Database connection successful")
#         else:
#             print("⚠️  Database connection issues")
            
#     except Exception as e:
#         print(f"❌ Error importing app: {e}")
#         import traceback
#         traceback.print_exc()
#         sys.exit(1)
    
#     print("\n🚀 Starting server...")
#     print("📡 Access URLs:")
#     print("   Local: http://localhost:8000")
#     print("   Docs: http://localhost:8000/docs")
#     print("="*60)
    
#     uvicorn.run(
#         "app.main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True,
#         log_level="info"
#     )











# # run_auth.py
# import uvicorn
# import sys
# import os

# # Add the project root to Python path
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# if __name__ == "__main__":
#     print("\n" + "="*60)
#     print("🔐 AUTH TEST SERVER")
#     print("="*60)
#     print("\nThis server tests ONLY authentication endpoints")
#     print("Testing endpoints:")
#     print("  1. GET  /auth/health")
#     print("  2. POST /auth/register")
#     print("  3. POST /auth/login")
#     print("  4. GET  /auth/me (requires JWT)")
#     print("\nStarting server...")
#     print("="*60)
    
#     uvicorn.run(
#         "app.main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True,
#         log_level="info"
#     )












# run_auth.py
import uvicorn
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔐 AUTH TEST SERVER")
    print("="*60)
    print("\nThis server tests ONLY authentication endpoints")
    print("Testing endpoints:")
    print("  1. GET  /auth/health")
    print("  2. POST /auth/register")
    print("  3. POST /auth/login")
    print("  4. GET  /auth/me (requires JWT)")
    print("\nStarting server...")
    print("="*60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )