# import uvicorn
# from app import app

# if __name__ == "__main__":
#     uvicorn.run(
#         "run:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True
#     )


# run.py (in root directory)
"""
Launch script for the FastAPI application.
Run with: python run.py
Or use: uvicorn run:app --reload
"""
import uvicorn
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting Healthy Recommender Backend...")
    print("✅ All API keys configured")
    print("📚 Swagger UI available at: http://127.0.0.1:8000/docs")
    print("📖 ReDoc available at: http://127.0.0.1:8000/redoc")
    print("🔧 Debug mode: ON")
    print("⏳ Starting server...\n")
    
    # Start the server
    uvicorn.run(
        "app.main:app",  # Import string for reload to work
        host="0.0.0.0",  # Listen on all interfaces
        port=8000,
        reload=True,     # Enable auto-reload on code changes
        reload_dirs=["app"],  # Watch only app directory for changes
        log_level="info"
    )