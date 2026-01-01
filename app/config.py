
# # app/config.py
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Settings:
#     # ========== NEON POSTGRESQL ==========
#     # Use YOUR Neon URL from .env or hardcode it
#     DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_adJ8QvFxsD4H@ep-twilight-poetry-ad9esqb5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require")
    
#     # For backward compatibility
#     POSTGRES_URL = DATABASE_URL
#     DATABASE_TYPE = "neon"
    
#     # ========== API KEYS ==========
#     GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
#     # ========== SERVER ==========
#     HOST = os.getenv("HOST", "0.0.0.0")
#     PORT = int(os.getenv("PORT", 8000))
#     DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
#     # ========== GEMINI ==========
#     GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# settings = Settings()

# # Print debug info
# print(f"⚙️ Config loaded")
# print(f"🔗 Database URL set: {'Yes' if settings.DATABASE_URL else 'No'}")










# # app/config.py
# """
# Application Configuration
# Loads environment variables from .env file
# """

# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()


# class Settings:
#     """Application settings loaded from environment variables"""
    
#     # ============================================================
#     # DATABASE CONFIGURATION
#     # ============================================================
#     DATABASE_URL: str = os.getenv(
#         "DATABASE_URL",
#         ""
#     )
    
#     # ============================================================
#     # JWT AUTHENTICATION CONFIGURATION
#     # ============================================================
#     SECRET_KEY: str = os.getenv(
#         "SECRET_KEY",
#         "your-fallback-secret-key-change-this-in-production"
#     )
    
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
#         os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
#     )
    
#     ALGORITHM: str = "HS256"
    
#     # ============================================================
#     # API KEYS
#     # ============================================================
#     GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
#     GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
#     # ============================================================
#     # GEMINI AI CONFIGURATION
#     # ============================================================
#     GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
#     # ============================================================
#     # SERVER CONFIGURATION
#     # ============================================================
#     PORT: int = int(os.getenv("PORT", "8000"))
#     DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
#     HOST: str = os.getenv("HOST", "0.0.0.0")
    
#     # ============================================================
#     # CORS CONFIGURATION
#     # ============================================================
#     ALLOWED_ORIGINS: list = [
#         "http://localhost:3000",
#         "http://localhost:5173",
#         "http://localhost:8080",
#         "*"  # Remove in production, specify exact domains
#     ]


# # Create settings instance
# settings = Settings()


# # ============================================================
# # CONFIGURATION VALIDATION
# # ============================================================

# def validate_config():
#     """Validate critical configuration settings"""
#     issues = []
    
#     if not settings.DATABASE_URL:
#         issues.append("⚠️  DATABASE_URL not set in .env")
    
#     if not settings.SECRET_KEY or settings.SECRET_KEY == "your-fallback-secret-key-change-this-in-production":
#         issues.append("⚠️  SECRET_KEY not set or using default (security risk)")
    
#     if not settings.GOOGLE_API_KEY:
#         issues.append("⚠️  GOOGLE_API_KEY not set in .env")
    
#     if not settings.GEMINI_API_KEY:
#         issues.append("⚠️  GEMINI_API_KEY not set in .env")
    
#     return issues


# # ============================================================
# # STARTUP CONFIGURATION CHECK
# # ============================================================

# # Print configuration status on import
# if __name__ != "__main__":
#     print("⚙️  Configuration loaded:")
#     print(f"   Database: {'✅ Connected' if settings.DATABASE_URL else '❌ Not configured'}")
#     print(f"   JWT Secret: {'✅ Set' if settings.SECRET_KEY and settings.SECRET_KEY != 'your-fallback-secret-key-change-this-in-production' else '❌ Not set or default'}")
#     print(f"   Google API: {'✅ Set' if settings.GOOGLE_API_KEY else '❌ Not set'}")
#     print(f"   Gemini API: {'✅ Set' if settings.GEMINI_API_KEY else '❌ Not set'}")




# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # ========== DATABASE ==========
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    
    # ========== JWT ==========
    SECRET_KEY = os.getenv("SECRET_KEY", "your-fallback-secret-key-for-development-12345")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # ========== API KEYS ==========
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # ========== SERVER ==========
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # ========== GEMINI ==========
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

settings = Settings()

# Debug info
print(f"⚙️ Config loaded:")
print(f"   Database URL: {'Set' if settings.DATABASE_URL else 'Not set'}")
print(f"   JWT Secret: {'Set' if settings.SECRET_KEY and settings.SECRET_KEY != 'your-fallback-secret-key-for-development-12345' else 'Using fallback'}")
print(f"   Google API: {'Set' if settings.GOOGLE_API_KEY else 'Not set'}")
print(f"   Gemini API: {'Set' if settings.GEMINI_API_KEY else 'Not set'}")