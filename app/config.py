
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Settings:
#     # API Keys
#     GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
#     GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
#     # MongoDB
#     MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
#     DB_NAME: str = os.getenv("DB_NAME", "recommendation_db")
    
#     # Server
#     HOST: str = os.getenv("HOST", "0.0.0.0")
#     PORT: int = int(os.getenv("PORT", 8000))
#     DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
#     # Gemini Configuration
#     GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
#     def validate(self):
#         """Validate required settings"""
#         missing = []
#         if not self.GOOGLE_API_KEY:
#             missing.append("GOOGLE_API_KEY")
#         if not self.GEMINI_API_KEY:
#             missing.append("GEMINI_API_KEY")
        
#         if missing:
#             raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# settings = Settings()

# # Validate on import
# try:
#     settings.validate()
#     print("✅ All API keys configured")
# except ValueError as e:
#     print(f"❌ Configuration Error: {e}")
#     exit(1)
# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database Configuration
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "neon")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # For backwards compatibility
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "")
    
    # MongoDB (for migration only)
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "recommendation_db")
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Gemini
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    def validate(self):
        """Validate required settings"""
        missing = []
        if not self.DATABASE_URL and not self.POSTGRES_URL:
            missing.append("DATABASE_URL or POSTGRES_URL")
        if not self.GOOGLE_API_KEY:
            missing.append("GOOGLE_API_KEY")
        if not self.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

settings = Settings()